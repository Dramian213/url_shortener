# URL Shortener API

🇬🇧 [English version](README.md)

REST API do skracania linków z autentykacją JWT, statystykami kliknięć i rate limitingiem, zbudowane w FastAPI.

## Funkcje

- Skracanie długich URL-i do krótkich, unikalnych kodów
- Przekierowanie ze skróconego linku na oryginalny adres
- Statystyki kliknięć dla każdego linku
- Rejestracja i logowanie użytkowników (JWT)
- Linki przypisane do konkretnego użytkownika (`GET /my_urls`)
- Rate limiting na wrażliwych endpointach (login, register, shorten)
- Automatyczna dokumentacja API (Swagger UI)

## Stack technologiczny

- **FastAPI** — framework webowy
- **PostgreSQL** — baza danych
- **SQLAlchemy** — ORM
- **Alembic** — migracje bazy danych
- **Docker + Docker Compose** — konteneryzacja
- **JWT (python-jose)** — autentykacja
- **Passlib (bcrypt)** — hashowanie haseł
- **SlowAPI** — rate limiting

## Uruchomienie lokalnie

Wymagania: Docker Desktop.

1. Sklonuj repozytorium:
```bash
   git clone https://github.com/Dramian213/url_shortener.git
   cd url_shortener
```

2. Stwórz plik `.env` w głównym katalogu:
```bash
    DATABASE_URL=postgresql://postgres:postgres@db:5432/url_shortener
    SECRET_KEY=twoj-tajny-klucz
```

3. Uruchom kontenery:
```bash
   docker compose up --build
```

4. Zastosuj migracje bazy danych:
```bash
   docker compose exec app alembic upgrade head
```

5. Otwórz dokumentację API: [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpointy

| Metoda |         Ścieżka        |              Opis                |
|--------|------------------------|----------------------------------|
| POST   | `/register`            | Rejestracja nowego użytkownika   |
| POST   | `/login`               | Logowanie, zwraca token JWT      |
| POST   | `/shorten`             | Tworzy skrócony link   !         | 
| GET    | `/my_urls`             | Lista linków użytkownika  !      | 
| GET    | `/{short_code}`        | Przekierowanie na oryginalny URL |
| GET    | `/stats/{short_code}`  | Statystyki kliknięć linku        |
| GET    | `/health`              | Healthcheck                      |

### Legenda

Wymaga logowania - !

## Czego się nauczyłem

Ten projekt był moim pierwszym pełnym API budowanym od zera — obejmuje konteneryzację, migracje bazy danych, autentykację JWT i podstawy zabezpieczeń API (hashowanie haseł, rate limiting).