# Content Management System

A RESTful backend service for managing articles with user authentication and view tracking.

## Features

- User authentication with JWT tokens
- CRUD operations for articles
- Recently viewed articles tracking
- Pagination support
- Database schema management with Alembic
- Docker support for easy deployment

## Local Setup

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

## Docker Setup

1. Set up environment variables (optional):
   Create a `.env` file with the following variables:

   ```env
   SECRET_KEY=your-secure-secret-key
   POSTGRES_PASSWORD=your-secure-db-password
   ```

2. Build and run with Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Environment Variables

- `SECRET_KEY`: JWT secret key (default: your-secret-key-here)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `SQLALCHEMY_DATABASE_URL`: postgresql://postgres:postgres@db:5432/cms

## API Endpoints

### Authentication

- `POST /users/`: Create a new user
- `POST /token`: Login and get access token

### Articles

- `GET /articles/`: List all articles
- `POST /articles/`: Create a new article
- `GET /articles/{id}`: Get article details
- `PUT /articles/{id}`: Update an article
- `DELETE /articles/{id}`: Delete an article
- `GET /articles/recent/`: Get recently viewed articles
