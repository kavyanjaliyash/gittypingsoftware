"""
SMS Delivery Gateway Utility.
Supports Fast2SMS, Twilio, MSG91, and Console (Development Mock).
Handles mobile number normalization and masking.
"""

import os
import re
import urllib.parse
import urllib.request
import json

def normalize_mobile(phone_str):
    """
    Normalizes and validates an Indian mobile number.
    Returns 10-digit mobile string if valid, otherwise None.
    """
    if not phone_str:
        return None

    # Remove all non-digit characters
    digits = re.sub(r'\D', '', str(phone_str))

    # Strip country code / leading zeros if present
    if len(digits) == 12 and digits.startswith('91'):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith('0'):
        digits = digits[1:]

    # Check for valid 10-digit Indian mobile format (starts with 6, 7, 8, or 9)
    if len(digits) == 10 and re.match(r'^[6-9]\d{9}$', digits):
        return digits

    return None

def mask_mobile(phone_str):
    """
    Masks mobile number for privacy (e.g., 9945023157 -> ******3157).
    """
    norm = normalize_mobile(phone_str)
    if norm:
        return '*' * 6 + norm[-4:]
    return '******'

def send_otp_sms(mobile_number, otp_code):
    """
    Sends an OTP SMS via the configured provider.
    Returns (success: bool, message: str).
    """
    norm_mobile = normalize_mobile(mobile_number)
    if not norm_mobile:
        return False, "Invalid mobile number format."

    provider = os.environ.get("SMS_PROVIDER", "console").lower().strip()
    api_key = os.environ.get("SMS_API_KEY", "").strip()
    api_secret = os.environ.get("SMS_API_SECRET", "").strip()
    sender_id = os.environ.get("SMS_SENDER_ID", "").strip()
    template_id = os.environ.get("SMS_TEMPLATE_ID", "").strip()

    masked = mask_mobile(norm_mobile)

    # 1. Console / Development Provider
    if provider == "console" or not api_key:
        print(f"[SMS Gateway Console] Sent OTP '{otp_code}' to {masked} (Provider: {provider})")
        return True, "OTP dispatched successfully."

    # 2. Fast2SMS Provider (India)
    if provider == "fast2sms":
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {
                "authorization": api_key,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            payload = {
                "variables_values": str(otp_code),
                "route": "otp",
                "numbers": norm_mobile
            }
            data = urllib.parse.urlencode(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                if result.get("return") is True:
                    print(f"[SMS Gateway Fast2SMS] OTP sent successfully to {masked}.")
                    return True, "OTP dispatched successfully."
                else:
                    msg = result.get("message", ["Delivery failed"])[0] if isinstance(result.get("message"), list) else result.get("message", "Delivery failed")
                    print(f"[SMS Gateway Error] Fast2SMS failure: {msg}")
                    return False, f"SMS Delivery error: {msg}"
        except Exception as e:
            print(f"[SMS Gateway Exception] Fast2SMS error: {e}")
            return False, f"SMS Gateway connection error: {e}"

    # 3. Twilio Provider
    if provider == "twilio":
        try:
            if not api_secret or not sender_id:
                return False, "Twilio configuration missing SMS_API_SECRET (Account SID) or SMS_SENDER_ID."

            url = f"https://api.twilio.com/2010-04-01/Accounts/{api_secret}/Messages.json"
            to_number = f"+91{norm_mobile}"
            message_body = f"Your Global IT Typing Software password reset OTP is {otp_code}. Valid for 10 minutes."
            payload = {
                "To": to_number,
                "From": sender_id,
                "Body": message_body
            }
            data = urllib.parse.urlencode(payload).encode('utf-8')

            import base64
            auth_str = f"{api_secret}:{api_key}"
            b64_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
            headers = {
                "Authorization": f"Basic {b64_auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status in [200, 201]:
                    print(f"[SMS Gateway Twilio] OTP sent successfully to {masked}.")
                    return True, "OTP dispatched successfully."
                else:
                    return False, "Twilio dispatch failed."
        except Exception as e:
            print(f"[SMS Gateway Exception] Twilio error: {e}")
            return False, f"Twilio SMS Gateway error: {e}"

    # 4. MSG91 Provider
    if provider == "msg91":
        try:
            url = f"https://api.msg91.com/api/v5/otp?template_id={template_id}&mobile=91{norm_mobile}&otp={otp_code}"
            headers = {
                "authkey": api_key,
                "Content-Type": "application/json"
            }
            req = urllib.request.Request(url, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                if result.get("type") == "success":
                    print(f"[SMS Gateway MSG91] OTP sent successfully to {masked}.")
                    return True, "OTP dispatched successfully."
                else:
                    return False, f"MSG91 error: {result.get('message')}"
        except Exception as e:
            print(f"[SMS Gateway Exception] MSG91 error: {e}")
            return False, f"MSG91 SMS Gateway error: {e}"

    # Fallback / Default
    print(f"[SMS Gateway Console] Fallback OTP '{otp_code}' for {masked}")
    return True, "OTP dispatched."
