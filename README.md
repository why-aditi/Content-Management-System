# Content Management System

A RESTful backend service for managing articles with user authentication and view tracking.

## Features

- User authentication with JWT tokens
- CRUD operations for articles
- Recently viewed articles tracking
- Pagination support
- Database schema management with Alembic

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication

- `POST /users/`: Create a new user
- `POST /token`: Login and get access token

### Articles

- `POST /articles/`: Create a new article
- `GET /articles/`: List user's articles (with pagination)
- `GET /articles/{article_id}`: Get article details
- `PUT /articles/{article_id}`: Update article
- `DELETE /articles/{article_id}`: Delete article

### User

- `GET /users/me/`: Get current user information

## Authentication

All article-related endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Pagination

The articles list endpoint supports pagination with `skip` and `limit` query parameters:

```
GET /articles/?skip=0&limit=10
```
