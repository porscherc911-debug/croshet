# Tiny Hook Tales

A Django-based crochet store and admin dashboard.

## Local development

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Production deployment

This project is configured for Render deployment with PostgreSQL.

Required environment variables:

```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DATABASE
```

Render build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Render start command:

```bash
gunicorn croshet.wsgi:application
```

## Project structure

```text
croshet/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── croshet/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── admin/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── admin/
│           └── admin.html
├── user/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── user/
│           └── user.html
└── db.sqlite3
```

## Git flow

```bash
git init
git add .
git commit -m "Deploy-ready Django project"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
