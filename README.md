Smart Device Discovery Platform (Django + MongoDB)

A backend-driven web application for filtering and exploring smartphone data using real-world datasets.
Built with Django and MongoDB, focusing on data ingestion, querying, and scalable filtering.

Features

Server-side filtering by:

Brand

Price

RAM

Storage

Processor

Display

Front Camera

Back Camera

Battery

Dependent (cascading) filters

Selecting a brand updates available processors, displays, cameras, and RAM/storage combinations.

Pagination (10 devices per page)

CSV → MongoDB data ingestion

Clean query construction using MongoDB operators

Tech Stack

Backend: Django (Python)

Database: MongoDB

Frontend: HTML, CSS, JavaScript

Data Processing: Pandas

Tools: MongoDB Compass, Git

Architecture (High Level)
Browser
  ↓
Django Templates
  ↓
Django Views
  ↓
MongoDB Queries (filters + pagination)
  ↓
MongoDB (devices collection)

Project Structure
smart_device_recommender/
├── manage.py
├── requirements.txt
├── README.md
├── smart_device_recommender/
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── devices/
│   │   ├── views.py
│   │   └── urls.py
│   ├── recommendations/
│   │   ├── rules.py
│   │   └── urls.py
│   │   └── view.py
│   └── core/
│       └── db.py
├── templates/
│   └── home.html
│   └── result.html
├── static/
│   └── css/
├── data/
│   └── import_csv_to_mongo.py
└── venv/ (gitignored)

Dataset

Smartphone specifications dataset (CSV)

Preprocessing steps:

Column renaming

Data cleaning

Type normalization

Bulk insertion into MongoDB

Key Implementation Details
Dependent Filters

Dropdown options are populated using MongoDB distinct() queries scoped by brand.

device_collection.distinct("processor", {"brand": /Samsung/i})

Pagination
device_collection.find(query).skip(offset).limit(10)

Filtering

Filters are dynamically applied based on query parameters to avoid unnecessary conditions.

Running Locally
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python manage.py runserver


Open: http://127.0.0.1:8000/
