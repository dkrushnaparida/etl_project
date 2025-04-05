# Django ETL Project

This Django project allows uploading sales data CSVs from two regions, applies ETL transformations, stores them in SQLite, and displays analytics with pagination and dashboards.

### 🔧 Features
- Upload 2 CSVs (Region A & B)
- ETL: clean, transform, calculate totals
- Store in SQLite DB
- Display sales data in UI with pagination
- Validation dashboard using raw SQL
- Admin panel for uploads & data

### 🚀 Tech Stack
- Python 3.12
- Django 5.2
- SQLite
- Pandas

### 📦 To Run Locally
```bash
git clone https://github.com/dkrushnaparida/etl_project.git
cd etl_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
