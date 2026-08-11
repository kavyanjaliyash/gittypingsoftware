// Nudi keyboard mapping rules & reverse lookup table
const NUDI_MAP = {
    'a': 'ಅ', 'A': 'ಆ', 'i': 'ಇ', 'I': 'ಈ', 'u': 'ಉ', 'U': 'ಊ',
    'R': 'ಋ', 'e': 'ಎ', 'E': 'ಏ', 'Y': 'ಐ', 'o': 'ಒ', 'O': 'ಓ', 'V': 'ಔ',
    'M': 'ಂ', 'H': 'ಃ', 'f': '್',
    'k': 'ಕ್', 'K': 'ಖ್', 'g': 'ಗ್', 'G': 'ಘ್',
    't': 'ಟ್', 'T': 'ಠ್', 'd': 'ಡ್', 'D': 'ಢ್', 'N': 'ಣ್',
    'p': 'ಪ್', 'P': 'ಫ್', 'b': 'ಬ್', 'B': 'ಭ್', 'm': 'ಮ್',
    'y': 'ಯ್', 'r': 'ರ್', 'l': 'ಲ್', 'v': 'ವ್', 's': 'ಸ್', 'x': 'ಷ್', 'S': 'ಶ್', 'h': 'ಹ್'
};

window.nudiReverseMap = {
    // Independent Vowels (ಸ್ವರಗಳು)
    'ಅ': 'a',
    'ಆ': 'A',
    'ಇ': 'i',
    'ಈ': 'I',
    'ಉ': 'u',
    'ಊ': 'U',
    'ಋ': 'R',
    'ೠ': 'R',
    'ಎ': 'e',
    'ಏ': 'E',
    'ಐ': 'Y',
    'ಒ': 'o',
    'ಓ': 'O',
    'ಔ': 'V',
    'ಅಂ': 'aM',
    'ಅಃ': 'aH',

    // Dependent Vowel Signs / Matras (ಗುಣಿತಾಕ್ಷರ ಚಿಹ್ನೆಗಳು)
    '\u0CBE': 'A',  // ಾ (Vowel sign AA)
    '\u0CBF': 'i',  // ಿ (Vowel sign I)
    '\u0CC0': 'I',  // ೀ (Vowel sign II)
    '\u0CC1': 'u',  // ು (Vowel sign U)
    '\u0CC2': 'U',  // ೂ (Vowel sign UU)
    '\u0CC3': 'R',  // ೃ (Vowel sign Vocalic R)
    '\u0CC4': 'R',  // ೄ (Vowel sign Vocalic RR)
    '\u0CC6': 'e',  // ೆ (Vowel sign E)
    '\u0CC7': 'E',  // ೇ (Vowel sign EE)
    '\u0CC8': 'Y',  // ೈ (Vowel sign AI)
    '\u0CCA': 'o',  // ೊ (Vowel sign O)
    '\u0CCB': 'O',  // ೋ (Vowel sign OO)
    '\u0CCC': 'V',  // ೌ (Vowel sign AU)
    '\u0CCD': 'f',  // ್ (Virama / Halanta)
    '\u0CD5': 'E',  // ೕ (Length mark)
    '\u0CD6': 'Y',  // ೖ (AI length mark)
    '\u0C82': 'M',  // ಂ (Anusvara)
    '\u0C83': 'H',  // ಃ (Visarga)
    '\u0CBC': 'F',  // ಼ (Nukta)

    // Kannada Consonants (ವ್ಯಂಜನಗಳು)
    'ಕ': 'k', 'ಖ': 'K', 'ಗ': 'g', 'ಘ': 'G', 'ಙ': 'W',
    'ಚ': 'c', 'ಛ': 'C', 'ಜ': 'j', 'ಝ': 'J', 'ಞ': 'z',
    'ಟ': 'q', 'ಠ': 'Q', 'ಡ': 'w', 'ಢ': 'W', 'ಣ': 'N',
    'ತ': 't', 'ಥ': 'T', 'ದ': 'd', 'ಧ': 'D', 'ನ': 'n',
    'ಪ': 'p', 'ಫ': 'P', 'ಬ': 'b', 'ಭ': 'B', 'ಮ': 'm',
    'ಯ': 'y', 'ರ': 'r', 'ಲ': 'l', 'ವ': 'v', 'ಶ': 'S',
    'ಷ': 'x', 'ಸ': 's', 'ಹ': 'h', 'ಳ': 'L',
    'ಱ': 'r', 'ೞ': 'l'
};

/**
 * Universal grapheme and Indic/Kannada Akshara cluster segmenter.
 * Correctly segments English, numbers, emojis, Kannada conjuncts (ಒತ್ತಕ್ಷರಗಳು - e.g. ಕ್ಕ, ಖ್ಖ, ಗ್ಗ, ಘ್ಘ, ಙ್ಙ),
 * and Indian orthographic syllables.
 */
window.segmentTextIntoGraphemes = function(text) {
    if (!text) return [];
    
    // Indic/Kannada syllable regex with full conjunct & sub-letter (ಒತ್ತಕ್ಷರ) support:
    // Matches (Consonant + Virama)* + Consonant/Vowel + Matras* + Virama? + Modifiers*
    const indicRegex = /(?:(?:[\u0900-\u0D7F](?:\u0CCD|\u094D|\u09CD|\u0A4D|\u0ACD|\u0B4D|\u0BCD|\u0C4D|\u0D4D)[\u200C\u200D]?)+[\u0900-\u0D7F][\u093E-\u094C\u0962\u0963\u0ABE-\u0ACC\u0B3E-\u0B4C\u0BBE-\u0BCC\u0C3E-\u0C4C\u0C55\u0C56\u0CBE-\u0CCC\u0CD5\u0CD6\u0D3E-\u0D4C\u0D57]?[\u0CCD|\u094D|\u09CD|\u0A4D|\u0ACD|\u0B4D|\u0BCD|\u0C4D|\u0D4D]?[\u0901-\u0903\u0A81-\u0A83\u0B01-\u0B03\u0B82\u0C01-\u0C03\u0C82\u0C83\u0D02\u0D03]?|[\u0900-\u0D7F][\u093E-\u094D\u0962\u0963\u0ABE-\u0ACD\u0B3E-\u0B4D\u0BBE-\u0BCD\u0C3E-\u0C4D\u0C55\u0C56\u0CBE-\u0CCD\u0CD5\u0CD6\u0D3E-\u0D4D\u0D57]*[\u0901-\u0903\u0A81-\u0A83\u0B01-\u0B03\u0B82\u0C01-\u0C03\u0C82\u0C83\u0D02\u0D03]?|[^\r\n]|\n)/gu;

    const matches = text.match(indicRegex);
    if (matches && matches.length > 0) {
        return matches;
    }

    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
        const seg = new Intl.Segmenter('kn', { granularity: 'grapheme' });
        return Array.from(seg.segment(text)).map(s => s.segment);
    }

    return Array.from(text);
};

/**
 * Converts a Kannada Akshara / text string into its exact sequence of English QWERTY Nudi keystrokes.
 * For English / Latin text, returns the characters directly.
 */
window.getNudiKeySequence = function(text) {
    if (!text) return "";
    let keys = "";
    for (const ch of text) {
        if (window.nudiReverseMap && window.nudiReverseMap[ch] !== undefined) {
            keys += window.nudiReverseMap[ch];
        } else {
            keys += ch;
        }
    }
    return keys;
};