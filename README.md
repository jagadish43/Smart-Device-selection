# Smart Device Discovery Platform

A Django + MongoDB web app for filtering and exploring smartphone data using real-world datasets.

---

## Features

- Server-side filtering by brand, price, RAM, storage, processor, display, camera, and battery
- Dependent (cascading) filters based on selected brand
- Pagination (10 devices per page)
- CSV data ingestion into MongoDB

---

## Tech Stack

- Django (Python)
- MongoDB
- HTML, CSS, JavaScript
- Pandas

---

## Architecture

```
Browser → Django Templates → Django Views → MongoDB → Results
```

---

## Screenshots

> Add screenshots of the application UI here.

```
screenshots/
├── home_page.png
├── filters_applied.png
└── pagination.png
```

Example:
```md
![Home Page](screenshots/home_page.png)
![Filters Applied](screenshots/filters_applied.png)
```

---

## Run Locally

```bash
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Open: http://127.0.0.1:8000/
