# URL Shortener API

🇵🇱 [Polska wersja](README.pl.md)

REST API for shortening URLs with JWT authentication, click statistics, and rate limiting, built with FastAPI.

## Features

- Shorten long URLs into unique short codes
- Redirect from short link to original URL
- Click statistics for each link
- User registration and login (JWT)
- Links tied to a specific user (`GET /my_urls`)
- Rate limiting on sensitive endpoints (login, register, shorten)
- Automatic API documentation (Swagger UI)

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Docker + Docker Compose** — containerization
- **JWT (python-jose)** — authentication
- **Passlib (bcrypt)** — password hashing
- **SlowAPI** — rate limiting

## Running locally

Requirements: Docker Desktop.

1. Clone the repository:
```bash
   git clone https://github.com/Dramian213/url_shortener.git
   cd url_shortener
```

2. Create a `.env` file in the root directory:
```bash
    DATABASE_URL=postgresql://postgres:postgres@db:5432/url_shortener
    SECRET_KEY=your-secret-key
```
3. Start the containers:
```bash
   docker compose up --build
```

4. Apply database migrations:
```bash
   docker compose exec app alembic upgrade head
```

5. Open the API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

| Method |         Path         |         Description              |
|--------|----------------------|----------------------------------|
| POST   | `/register`          | Register a new user              |
| POST   | `/login`             | Log in, returns a JWT            |
| POST   | `/shorten`           | Create a short link  !           |
| GET    | `/my_urls`           | List the logged-in user's links !|
| GET    | `/{short_code}`      | Redirect to the original URL     |
| GET    | `/stats/{short_code}`| Click statistics for a link      |
| GET    | `/health`            | Health check                     |

### Legend 

Auth required - !

## What I learned

This was my first full API built from scratch — covering containerization, database migrations, JWT authentication, and API security basics (password hashing, rate limiting).
