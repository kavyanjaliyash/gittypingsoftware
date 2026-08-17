# ⌨️ Kannada Typing Software

A web-based Kannada typing practice and examination platform featuring real-time Nudi phonetic layout transliteration, multi-level lessons, timed tests, and role-based administrative dashboards (Admin, Branch, Faculty, Student).

---

## 🚀 Running with Docker (Recommended)

### 1. Start Docker Desktop
Ensure **Docker Desktop** is running on your system.

### 2. Build & Start the Container
Run the following command from the project root:
```bash
docker compose up -d --build
```

### 3. Open in Browser
Visit **[http://localhost:5000](http://localhost:5000)** in your browser.

### Useful Docker Commands
* **View Logs:** `docker compose logs -f`
* **Stop Container:** `docker compose down`
* **Restart Container:** `docker compose restart`

> **Note on Data Persistence:** Database files are mapped to the local `./instance` folder, so your test results, registered students, and lessons remain intact even if the container is rebuilt or stopped.

---

## 💻 Running Locally without Docker

### 1. Set Up Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Application
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## 🔑 Default Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` |

*(Branches, Faculty, and Students can be created from the Admin/Branch dashboards.)*

---

## 📂 Project Structure

```
├── blueprints/         # Modular route blueprints (auth, admin, student, branch, faculty, demo)
├── instance/           # SQLite database persistence (typing.db)
├── static/
│   ├── css/            # UI styles and themes
│   └── js/             # Nudi engine & typing test logic
├── templates/          # Jinja2 HTML templates
├── app.py              # Application entry point & DB migrations
├── config.py           # Application configuration
├── database.py         # SQLAlchemy instance
├── models.py           # Database schema definitions
├── Dockerfile          # Container build definition
├── docker-compose.yml  # Container orchestration & volume mapping
├── requirements.txt    # Python package dependencies
└── README.md           # Documentation
```
