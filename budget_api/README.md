# Budget API - Personal Finance Management

This project is a RESTful API for managing personal finances, built with Django and Django Ninja. It supports importing OFX files, transaction reconciliation, and various financial reports.

## Features (Planned & Implemented)

*   OFX file import
*   Transaction categorization and reconciliation
*   Reporting (balance, expenses by category)
*   User management and authentication (Future)
*   PostgreSQL database

## Project Structure

```
budget_api/
├── api/                      # Main Django app for the API
│   ├── migrations/
│   ├── models/
│   ├── schemas/
│   ├── views/ (or routers/)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   └── urls.py               # For v1 API routes
├── config/                   # Django project configuration
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py               # Project root URLs
│   └── wsgi.py
├── .env-example              # Example environment variables
├── manage.py                 # Django's command-line utility
├── README.md                 # This file
└── requirements.txt          # Python package dependencies
```

## Getting Started

### Prerequisites

*   Python 3.9+
*   PostgreSQL
*   Poetry (optional, for dependency management if you prefer) or pip

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd budget_api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Copy `.env-example` to `.env`:
        ```bash
        cp .env-example .env
        ```
    *   Edit `.env` and provide your actual database credentials and a new `SECRET_KEY`.
        ```env
        DEBUG=True
        SECRET_KEY=your-super-secret-django-key-here-generate-a-new-one
        DATABASE_URL=postgres://your_db_user:your_db_password@your_db_host:your_db_port/your_db_name
        ALLOWED_HOSTS=127.0.0.1,localhost
        ```
    *   **Important for `SECRET_KEY`**: You can generate a new Django secret key using the following Python snippet:
        ```python
        from django.core.management.utils import get_random_secret_key
        print(get_random_secret_key())
        ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for Django Admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API should now be running at `http://127.0.0.1:8000/`.

## API Endpoints

### Health & Documentation

*   **`GET /public/health`**: System health check. Returns `{"status": "UP!"}`.
*   **`GET /public/ready`**: System readiness check (includes database connectivity).
*   **`GET /public/docs/`**: Swagger UI for public endpoints.
*   **`GET /api/v1/docs/`**: Swagger UI for version 1 API endpoints.

### Version 1 API (`/api/v1/`)

*   *(Initial endpoints will be listed here as they are developed, e.g., OFX import, transactions, categories)*
*   `GET /api/v1/sample`: A sample endpoint to verify v1 API is working.

## Running Tests

*(Instructions for running tests with pytest will be added here later)*

## TODO:

*   [ ] Create authentication basic by API Key
*   [ ] Optimize the parser OFX (Initial OFX parsing logic)
*   [ ] Implement cache in endpoints de relatório
*   [ ] Testes automatizados com `pytest`
*   [ ] Define complete models for `Lancamento`, `Categoria`, `Origem`, etc.
*   [ ] Implement `POST /api/v1/ofx-import` endpoint.
*   [ ] Implement `PUT /api/v1/lancamentos/{id}/conciliar` endpoint.
*   [ ] Implement `DELETE /api/v1/lancamentos/{id}/ignorar` endpoint.
*   [ ] Implement `GET /api/v1/lancamentos` (with filters).
*   [ ] Implement `PUT /api/v1/lancamentos/{id}` (full edit).
*   [ ] Implement auxiliary endpoints:
    *   [ ] `GET /api/v1/lancamentos/pendentes`
    *   [ ] `GET /api/v1/lancamentos/{id}`
    *   [ ] `GET /api/v1/categorias`
    *   [ ] `GET /api/v1/categorias/{id}/subcategorias`
    *   [ ] `GET /api/v1/origens`
*   [ ] Implement report endpoints:
    *   [ ] `GET /api/v1/relatorios/saldo-por-referencia`
    *   [ ] `GET /api/v1/relatorios/gastos-por-categoria`
*   [ ] Implement standardized JSON:API responses.
