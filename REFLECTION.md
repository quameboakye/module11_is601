# Module 10 Project Reflection

## Introduction

This project focused on implementing a secure user model, validating user input with Pydantic, testing database functionality, and preparing a FastAPI application for Docker-based deployment.

The work combined application development, database configuration, automated testing, containerization, and CI/CD practices.

## What I Implemented

I worked with SQLAlchemy to implement a user model containing a UUID primary key, username, email, password hash, account status fields, and timestamps.

I implemented unique constraints for usernames and email addresses to prevent duplicate accounts.

For password security, the application hashes passwords before storing them and verifies submitted passwords against the stored hashes. The database stores the password in a `password_hash` column rather than a plaintext password column.

I also worked with Pydantic schemas to validate user information, including email addresses and password requirements. The response schema excludes sensitive password fields.

## Database Challenges and Solutions

One important challenge was identifying that the application initially had two separate SQLAlchemy declarative Base objects. This meant that the database metadata used by the application did not consistently register the user table.

I corrected the model and database initialization imports so they use the same Base object. I then verified that the users table was registered in SQLAlchemy metadata and that PostgreSQL contained the expected columns.

Another challenge was a PostgreSQL port conflict. A different PostgreSQL container was already using host port 5432. Rather than stopping that existing database, I changed the project container's host mapping to port 5433 while retaining port 5432 inside the container.

I also updated the database schema from `password` to `password_hash` and verified that the migration preserved the existing unique constraints.

## Testing and Quality Assurance

I used Pytest to run the project's unit, integration, and end-to-end tests.

The tests cover database operations, uniqueness constraints, authentication, password hashing, Pydantic validation, and application functionality.

The latest verified local test run produced:

- 76 passing tests.
- 97.27% total code coverage.
- A configured minimum coverage threshold of 90%.

I also verified that the FastAPI health endpoint returned HTTP 200 and that the application container could connect to PostgreSQL.

The schema verification confirmed that the `users` table was registered correctly and that the database contained `password_hash`, rather than a `password` column.

## Docker and Deployment

I used Docker Compose to run the FastAPI application, PostgreSQL 16, and pgAdmin.

I verified that the application container started successfully, the PostgreSQL database was healthy, and the application could connect to the database.

The Dockerfile uses a Python slim base image and runs the application as a non-root user. It also includes a health check.

The GitHub Actions workflow is configured to automate the testing and Docker deployment process, including security scanning and Docker Hub publishing. A successful remote publication must be confirmed through the GitHub Actions run and Docker Hub repository before it can be reported as completed.

## Lessons Learned

This project reinforced several important software engineering practices:

1. **Database consistency matters.** SQLAlchemy models and database initialization must use the same metadata registry.
2. **Password security is essential.** Applications should store password hashes, not raw passwords.
3. **Validation improves data quality.** Pydantic helps reject invalid input before it reaches application logic.
4. **Automated tests provide confidence.** A comprehensive test suite helps identify regressions when changing models and database configuration.
5. **Containerization requires careful configuration.** Port mappings, environment variables, health checks, and database readiness all affect successful deployment.
6. **CI/CD improves repeatability.** Automated testing and deployment reduce the amount of manual work required to deliver application changes.

## Areas for Further Improvement

There are several improvements I would make before using this application in production:

- Move the JWT signing secret into secure external configuration rather than hardcoding it in the model.
- Replace development database credentials with secure credentials.
- Add further authentication and authorization integration tests.
- Verify the complete GitHub Actions deployment and Docker Hub image pull process.
- Continue monitoring dependency and container vulnerabilities.

## Conclusion

Overall, this assignment gave me practical experience integrating SQLAlchemy, Pydantic, PostgreSQL, Pytest, Docker, and GitHub Actions.

The successful local test run, database verification, and Docker Compose checks demonstrate that the core application and database configuration are functioning as expected. The project also highlighted the importance of consistent database metadata, secure password handling, and systematic verification during software development.
