# Django Endterm Project

A Django-based application for managing shops, items, categories, transactions, and user authentication. It includes features like background task processing with Celery, metrics collection with Prometheus, and visualization with Grafana.

## Features

- **User Authentication**:  
  Secure login and registration with JWT authentication.
  
- **Shop Management**:  
  Users can create and manage their own shops.

- **Item Management**:  
  Add, update, delete, and view items within a shop. Link items to categories.

- **Transactions**:  
  Perform buy, sell, and transfer transactions on items.

- **Photo Upload**:  
  Upload and manage photos for items.

- **Celery Integration**:  
  Asynchronous task processing (e.g., sending emails, background data processing).

- **Metrics Monitoring**:  
  Metrics exposed via Prometheus and visualized using Grafana.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (SimpleJWT)
- **Task Queue**: Celery, Redis
- **Monitoring**: Prometheus
- **Visualization**: Grafana
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (optional for containerized setup)

### Steps to Install

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/NursatSakyshev/django_endterm.git
    cd django_endterm
    ```

2. **Install Python Dependencies**:

    If you're not using Docker, install the dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up the Database**:

    Run migrations to set up your PostgreSQL database:
    ```bash
    python manage.py migrate
    ```

4. **Run the Application**:

    Start the development server:
    ```bash
    python manage.py runserver
    ```

    Your application should now be running at `http://localhost:8000`.

### Docker Setup (Optional)

1. **Build the Docker Image**:
    ```bash
    docker-compose up --build
    ```

2. **Run the Application**:

    Access the app at `http://localhost:8000`, Prometheus at `http://localhost:9090`, and Grafana at `http://localhost:3000`.

## API Endpoints

- **Authentication**:
  - `POST /api/token/`: Login and get tokens (JWT authentication).
  - `POST /api/token/refresh/`: Refresh access token.

- **User and Shop Management**:
  - `GET /api/shops/`: List shops.
  - `POST /api/shops/`: Create a new shop.
  - `GET /api/shops/{id}/`: Retrieve, update, or delete a specific shop.

- **Item Management**:
  - `GET /api/items/`: List all items.
  - `POST /api/items/`: Create a new item.
  - `GET /api/items/{id}/`: Retrieve, update, or delete a specific item.

- **Transaction Management**:
  - `POST /api/items/{id}/transaction/`: Perform a transaction on an item (buy, sell, transfer).

- **Photo Management**:
  - `POST /api/items/{id}/photos/`: Upload photos for an item.
  - `GET /api/items/{id}/photos/`: List all photos for an item.

## Monitoring with Prometheus and Grafana

- **Prometheus**: Metrics are exposed at `http://localhost:8000/metrics/` and scraped by Prometheus for monitoring.
- **Grafana**: Visualize Prometheus metrics with pre-configured dashboards in Grafana.

## Background Task Processing with Celery

Celery is used for handling background tasks asynchronously. Example tasks include sending email notifications and processing data.

### Celery Configuration:

- Install Celery and Redis:
  ```bash
  pip install celery redis
  ```
-  Run the Celery worker:

  ```bash 
  celery -A endterm worker --loglevel=info
    ```
  
-  Run the Celery beat:

  ```bash 
  celery -A endterm beat --loglevel=info
    ```