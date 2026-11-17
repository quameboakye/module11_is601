# Module 11 Project Reflection

## Introduction

Module 11 focused on developing, testing, containerizing, and deploying a FastAPI application with database integration and automated CI/CD. The project brought together Python, SQLAlchemy, Pydantic, PostgreSQL, Pytest, Docker, GitHub Actions, and Docker Hub.

An important part of the assignment was implementing a calculation model that supports different arithmetic operations, validating application data, testing the application, and automating the deployment process.

## What I Implemented

The application includes:

- A FastAPI application with API endpoints and interactive API documentation.
- SQLAlchemy models for users and calculations.
- A polymorphic calculation model supporting addition, subtraction, multiplication, and division.
- Pydantic schemas for validating incoming data and structuring API responses.
- PostgreSQL database integration.
- Unit, integration, and end-to-end tests.
- Docker configuration for containerizing the application.
- GitHub Actions workflows for automated testing, security scanning, and Docker Hub deployment.

The calculation model uses SQLAlchemy inheritance to represent different calculation types. This helped me understand how related models can share common fields while implementing different operations.

## Challenges and Solutions

### SQLAlchemy Model and Database Configuration

One challenge was ensuring that the application models used the same SQLAlchemy declarative Base as the database configuration. Separate Base objects can cause model metadata and database table creation to become disconnected.

I corrected the imports so that the models and database initialization used the same Base. I then verified the model metadata and database table creation through the integration tests.

### PostgreSQL Port Conflict

I encountered a port conflict because another PostgreSQL container was already using the default host port 5432.

I resolved this by mapping the PostgreSQL container's internal port 5432 to host port 5433. This allowed the project to use its own database without disrupting the existing container configuration.

### Database Schema and Password Hashing

Another challenge involved ensuring that the database schema used the correct password field. The application stores password hashes rather than plain-text passwords.

I aligned the model and schema with the password_hash field and verified that the database retained the required unique constraints.

### GitHub Actions and Deployment

Configuring the CI/CD workflow required careful attention to the database connection settings, PostgreSQL service configuration, and Docker build process.

I corrected the workflow configuration and verified that all three GitHub Actions jobs completed successfully:

- Test: automated tests completed successfully.
- Security: the security scanning job completed successfully.
- Deploy: the Docker image was built and published to Docker Hub.

I also pulled the published image from Docker Hub and ran it in a separate test container. The container became healthy, and both the application health endpoint and interactive API documentation returned HTTP 200 responses.

## Testing and Quality Assurance

I used Pytest to test the application's functionality across unit, integration, and end-to-end test categories.

The latest verified local test results were:

- **121 tests passed**
- **96% total code coverage**
- **100% coverage for the Calculation model**
- **90% minimum coverage requirement**

These results gave me confidence that the application components were working together correctly. The tests also helped identify configuration and integration issues before deployment.

## Docker and Deployment

Docker provided a consistent environment for packaging and running the application.

I used Docker Compose for the development environment and GitHub Actions to automate the CI/CD process. The workflow performs testing, security scanning, and deployment of the Docker image.

The published image is available at:

https://hub.docker.com/r/slasha1982/module11_is601

I verified the deployment by pulling the latest image from Docker Hub and running it in a separate container. The container reported a healthy status.

I also tested the following endpoints:

- Application health check: HTTP 200
- Interactive API documentation: HTTP 200

This confirmed that the published image could be retrieved and that the application could start successfully outside the original development environment.

## Lessons Learned

This assignment improved my understanding of several important software development concepts:

1. **SQLAlchemy:** I gained practical experience with model relationships, inheritance, polymorphism, and database metadata.
2. **Pydantic:** I improved my understanding of data validation and schema design.
3. **Testing:** I learned the importance of unit, integration, and end-to-end testing, as well as measuring code coverage.
4. **Docker:** I gained experience building and running containerized applications.
5. **CI/CD:** I learned how GitHub Actions can automate testing, security scanning, and deployment.
6. **Troubleshooting:** I became more confident diagnosing database configuration, port conflicts, and deployment issues.

## Areas for Further Improvement

Although the application and deployment workflow are working, there are areas I would like to improve:

- Expand test coverage for additional calculation edge cases and error scenarios.
- Improve application configuration and secrets management.
- Add more comprehensive authentication and authorization integration tests.
- Continue monitoring dependencies and container vulnerabilities.
- Improve deployment monitoring and logging.

## Conclusion

Module 11 provided practical experience in developing and deploying a Python application using modern software engineering tools.

I successfully implemented the application models and schemas, integrated PostgreSQL, achieved 96% test coverage, and configured an automated CI/CD workflow. I also verified that the published Docker Hub image could be pulled and run successfully.

The assignment strengthened my understanding of the complete development process, from application implementation and testing to containerization and automated deployment.
