# Module 10: Secure User Model, Pydantic Validation, Database Testing and Docker Deployment

## Project Overview

This project demonstrates a FastAPI application with a SQLAlchemy user model, Pydantic validation, secure password hashing, database integration, automated testing, and Docker deployment.

The application includes:
- A SQLAlchemy `User` model with UUID primary keys.
- Unique username and email constraints.
- Secure password hashing using Passlib and bcrypt.
- Password verification during authentication.
- Pydantic schemas for validating user input and controlling response data.
- PostgreSQL database support.
- Automated unit, integration, and end-to-end tests.
- Docker-based application deployment and GitHub Actions CI/CD.

## Repository Links

- **GitHub:** https://github.com/quameboakye/assignment10_is601
- **Docker Hub:** https://hub.docker.com/r/slasha1982/assignment10_is601

## Technology Stack

- Python 3.11 (Docker image)
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL 16
- Passlib / bcrypt
- Pytest and pytest-cov
- Docker and Docker Compose
- GitHub Actions
- Trivy vulnerability scanning

## Project Structure

```text
assignment10_is601/
├── .github/
│   └── workflows/
│       └── test.yml
├── app/
│   ├── auth/
│   ├── models/
│   │   └── user.py
│   ├── operations/
│   ├── schemas/
│   │   ├── base.py
│   │   └── user.py
│   ├── config.py
│   ├── database.py
│   └── database_init.py
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── unit/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── pytest.ini
├── REFLECTION.md
└── README.md
```

## Prerequisites

Install the following:
- Python 3.11 or later
- Git
- Docker Engine and Docker Compose

Verify the installations:

```bash
python3 --version
git --version
docker --version
docker compose version
```

## Clone the Repository

```bash
git clone https://github.com/quameboakye/assignment10_is601.git
cd assignment10_is601
```

## Local Python Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Tests

Run the complete test suite:

```bash
pytest
```

Run tests with coverage reporting and the assignment's 90% minimum:

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

The latest verified local test result was:

- **76 tests passed**
- **97.27% total code coverage**
- Coverage requirement: 90%

The suite includes unit, integration, and end-to-end tests.

## Database and Docker Compose Setup

The project uses Docker Compose to run the FastAPI application, PostgreSQL, and pgAdmin.

Start the services:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

The development service endpoints are:

| Service | Address |
|---|---|
| FastAPI | http://localhost:8000 |
| FastAPI health check | http://localhost:8000/health |
| FastAPI interactive documentation | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |
| PostgreSQL host port | 5433 |

The PostgreSQL container listens internally on port 5432 and is mapped to host port 5433 to avoid conflicts with other local PostgreSQL containers.

Initialize the database tables:

```bash
docker compose exec -T web python -m app.database_init
```

Verify the users table:

```bash
docker compose exec -T db \
  psql -U postgres -d fastapi_db -c "\d users"
```

Check the application health endpoint:

```bash
curl -i http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Check application logs:

```bash
docker compose logs --tail=50 web
```

Stop the services:

```bash
docker compose down
```

This command does not remove named database volumes. To remove database volumes, use `docker compose down -v` only when you intentionally want to delete the stored development database data.

## Secure User Model and Validation

The SQLAlchemy user model includes:
- UUID primary key.
- First name and last name.
- Unique email address.
- Unique username.
- `password_hash` column.
- Account activation and verification fields.
- Login timestamp.
- Creation and update timestamps.

Raw passwords are hashed before storage. Password verification uses the stored hash rather than storing plaintext passwords.

The project uses Pydantic validation for:
- Email address format.
- Required user information.
- Password length and complexity.
- User response serialization.

The `UserRead` response schema is available as a backward-compatible alias of `UserResponse`. The response schema excludes both `password` and `password_hash`.

## Docker Image

The Dockerfile builds the FastAPI application using Python 3.11 slim.

It includes:
- Dependency installation.
- A non-root application user.
- A container health check.
- Uvicorn as the application server.

If the image has been published to Docker Hub, it can be pulled and run using:

```bash
docker pull slasha1982/assignment10_is601:latest

docker run --rm -p 8000:8000 \
  slasha1982/assignment10_is601:latest
```

Then visit:

http://localhost:8000/health

Docker Hub image publication should be verified against the actual repository and GitHub Actions run before treating deployment as complete.

## CI/CD Pipeline

The GitHub Actions workflow is located at:

`.github/workflows/test.yml`

The workflow is configured to automate testing and the Docker build, security scanning, and Docker Hub publishing process.

Docker Hub authentication uses GitHub repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Do not put Docker Hub credentials or other secrets directly in source code or commit them to GitHub.

## Security Considerations

This project is intended as an educational development and deployment exercise.

Before production use:
- Replace development database credentials with secure credentials.
- Store secrets outside source code.
- Configure a strong, externally managed JWT signing secret.
- Use HTTPS and appropriate production database access controls.
- Review container and dependency vulnerabilities regularly.

The current development Docker Compose credentials and application signing-key configuration must not be treated as production-ready.

## Submission Checklist

- [x] SQLAlchemy user model.
- [x] Unique email and username constraints.
- [x] Password hashing and verification.
- [x] Pydantic validation.
- [x] Response schema excludes password fields.
- [x] Unit, integration, and end-to-end tests.
- [x] Local PostgreSQL and Docker Compose verification.
- [x] Local test coverage above 90%.
- [ ] Confirm successful GitHub Actions Docker Hub deployment.
- [ ] Confirm published Docker Hub image can be pulled and run.
- [ ] Include screenshots of successful GitHub Actions and Docker Hub publication.
- [x] Project reflection document.

## Author

Repository owner: `quameboakye`
