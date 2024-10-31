# FastAPI E-Commerce API Project Guide

This guide outlines the architecture and directory structure of a FastAPI-based REST API for an e-commerce application. The project follows Domain-Driven Design (DDD), includes Docker for containerization, Poetry for dependency management, and `pytest` for testing.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Entities](#entities)
4. [Business Rules](#business-rules)
5. [Repositories](#repositories)
6. [Services](#services)
7. [Error Handling and HTTP Status Codes](#error-handling-and-http-status-codes)
8. [User Management](#user-management)
9. [API Structure](#api-structure)
10. [Endpoint Descriptions](#endpoint-descriptions)
11. [Dependency Injection](#dependency-injection)
12. [Dependencies](#dependencies)
13. [Configuration and Running the Application](#configuration-and-running-the-application)
14. [Testing](#testing)
15. [Code Style and Documentation](#code-style-and-documentation)
16. [Docker Integration](#docker-integration)

---

## Project Overview

The application implements a REST API with operations to:
- Manage products (CRUD operations with filtering and discount features).
- Handle user interactions (reservation, cancellation, sales).
- Track inventory and generate sales reports.

The API should support paginated responses and integrate Swagger for automatic documentation. Each component follows DDD principles, and the project is structured with clear separation of concerns.

---

## Directory Structure

```plaintext
online_store/
├── README.md
├── pyproject.toml
├── poetry.lock
├── .env
├── docs/
│   └── architecture_diagram.png
│
├── docker-compose/
│   ├── app.yaml
│   ├── Dockerfile
│
├── app/
│   ├── main.py                # FastAPI app instantiation
│   ├── containers.py          # Dependency injection setup
│   ├── config.py              # Configuration management
│   ├── __init__.py
│
│   ├── domain/                # Core business logic (Entities and Domain Services)
│   │   ├── entities/
│   │   │   ├── base_entity.py
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── reservation.py
│   │   │   ├── sale.py
│   │   │   └── __init__.py
│   │   ├── services/          # Domain-specific logic for each entity
│   │   │   ├── product_service.py
│   │   │   ├── category_service.py
│   │   │   ├── reservation_service.py
│   │   │   ├── sale_service.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│
│   ├── infrastructure/        # Data access and persistence (Database models, Repositories)
│   │   ├── repositories/
│   │   │   ├── base_repository.py
│   │   │   ├── product_repository.py
│   │   │   ├── category_repository.py
│   │   │   ├── reservation_repository.py
│   │   │   ├── sale_repository.py
│   │   │   └── __init__.py
│   │   ├── database/
│   │   │   ├── models.py       # SQLAlchemy models for database tables
│   │   │   ├── session.py      # Database session management
│   │   │   └── __init__.py
│   │   └── __init__.py
│
│   ├── application/            # Application logic (DTOs and Interfaces)
│   │   ├── dtos/
│   │   │   ├── product_dto.py
│   │   │   ├── category_dto.py
│   │   │   ├── reservation_dto.py
│   │   │   ├── sale_dto.py
│   │   │   └── __init__.py
│   │   ├── interfaces/         # Repository interfaces
│   │   │   ├── product_repository_interface.py
│   │   │   ├── category_repository_interface.py
│   │   │   ├── reservation_repository_interface.py
│   │   │   ├── sale_repository_interface.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│
│   ├── presentation/           # API layer (Endpoints and Schemas)
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── products.py
│   │   │   │   │   ├── categories.py
│   │   │   │   │   ├── reservations.py
│   │   │   │   │   ├── sales.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── dependencies.py  # Dependencies for API endpoints
│   │   │   └── __init__.py
│   │   ├── schemas/             # Pydantic schemas for validation
│   │   │   ├── product_schema.py
│   │   │   ├── category_schema.py
│   │   │   ├── reservation_schema.py
│   │   │   ├── sale_schema.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│
│   └── __init__.py
│
├── tests/                      # Test suite for the application
│   ├── conftest.py
│   ├── domain/
│   │   ├── entities/
│   │   ├── services/
│   │   └── __init__.py
│   ├── application/
│   │   └── __init__.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   └── __init__.py
│   ├── presentation/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── test_products.py
│   │   │       ├── test_categories.py
│   │   │       ├── test_reservations.py
│   │   │       ├── test_sales.py
│   │   │       └── __init__.py
│   │   └── __init__.py
│   └── __init__.py
└── ...
```


---

## Entities

### Purpose

Entities represent core business objects and their attributes. Each entity should be built with `dataclasses` and strongly typed using Python's `typing` module to define the data structure.

### Entities to Implement

- **Product**
  - Attributes: `id`, `name`, `category_id`, `price`, `stock`, `discount`.
  - Responsibilities: Stores details about individual products, price, stock level, and active discount percentage.

- **Category**
  - Attributes: `id`, `name`, `parent_category_id` (optional for subcategories).
  - Responsibilities: Organizes products into categories and subcategories for structured filtering.

- **Reservation**
  - Attributes: `id`, `product_id`, `quantity`, `status` (`reserved`, `cancelled`).
  - Responsibilities: Tracks product reservations and manages stock adjustments.

- **Sale**
  - Attributes: `id`, `product_id`, `quantity`, `sale_date`.
  - Responsibilities: Records product sales transactions for report generation and analysis.

---

## Business Rules

### Product Availability
- Products are only displayed if there is available stock.
- When a product is reserved or sold, the stock is adjusted accordingly:
  - **Reservation**: Temporarily decreases stock until the reservation is finalized or canceled.
  - **Sale**: Permanently reduces stock and records the transaction.
  - **Cancellation**: Restores stock to the previous level.


---

## Repositories

Repositories handle data access logic, interfacing with the database or in-memory data store. Each repository will be defined with a base interface in **`base_repository.py`** and specific implementations in individual repository files.

### Repositories to Implement

- **Base Repository**: Define basic CRUD methods (`get_all`, `get_by_id`, `add`, `update`, `delete`).
- **ProductRepository**: Manages products with additional methods like `apply_discount` and `filter_by_category`.
- **CategoryRepository**: Manages product categories, supports hierarchical data structure.
- **ReservationRepository**: Tracks reservations with stock management methods.
- **SaleRepository**: Records sales transactions and supports report generation.

### Database Integration

This project uses **PostgreSQL** as the primary database to store product, category, reservation, and sales data. PostgreSQL is containerized through Docker for ease of deployment.

---

## Services

Service classes encapsulate business logic and coordinate between repositories and entities.

### Services to Implement

- **ProductService**
  - Methods: `create_product`, `update_product_price`, `apply_discount`, `manage_stock`.
- **CategoryService**
  - Methods: `create_category`, `get_all_categories`, `filter_by_hierarchy`.
- **ReservationService**
  - Methods: `reserve_product`, `cancel_reservation`, `adjust_stock`.
- **SaleService**
  - Methods: `record_sale`, `generate_sales_report`.


---

## Error Handling and HTTP Status Codes

The API endpoints return the following HTTP status codes:

- **200 OK**: Successful retrieval or operation.
- **201 Created**: A new resource has been successfully created.
- **400 Bad Request**: Invalid input parameters.
- **404 Not Found**: Requested resource does not exist.
- **409 Conflict**: Conflict in request, e.g., attempting to reserve an out-of-stock product.
- **500 Internal Server Error**: Unhandled server error.

---

## User Management

This project does not currently implement user management. However, it can be added as a separate module in the future.

---

## API Structure

- **Main Application**: `main.py` initiates FastAPI app and includes routers.
- **Routers**:
  - `products.py`: Endpoints for product CRUD operations and filtering.
  - `categories.py`: Endpoints for category management and filtering.
  - `reservations.py`: Endpoints for managing product reservations.
  - `sales.py`: Endpoints for recording and reporting sales transactions.

---

## Endpoint Descriptions

### Products Endpoint (`/products`)
- **GET /products**: Retrieves a list of products with filtering options.
- **POST /products**: Adds a new product.

### Categories Endpoint (`/categories`)
- **GET /categories**: Lists all categories and subcategories.

### Reservations Endpoint (`/reservations`)
- **POST /reservations**: Reserves a product.

### Sales Endpoint (`/sales`)
- **POST /sales**: Completes a sale and updates stock.


---

## Dependency Injection

The project uses `punq` for dependency injection, ensuring a flexible and testable architecture. Dependencies, such as repositories and services, will be configured in **`dependencies.py`** and injected into API routes and service classes.

---

## Dependencies

- **Frameworks & Tools**: FastAPI, Uvicorn, punq, Poetry, Pytest, Dataclasses, Typing, Docker, SQLAlchemy (optional).

---

## Configuration and Running the Application

1. **Configuration File**: `config.py` loads environment variables and database URLs.

2. **Run locally with Poetry**:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

3. **Database Migrations** (if applicable):
   - Use Alembic or similar tool to handle migrations.

---

## Testing

1. **Testing Framework**: `pytest`.
2. **Test Strategy**:
   - Use in-memory repositories to isolate business logic tests.
   - Test all service methods and API endpoints.
3. **Directory**: Place all tests in the **`tests`** directory, with separate test files for products, categories, reservations, and sales.

### Running Tests
```bash
pytest
```

---

## Code Style and Documentation

- Adhere to **PEP 8** guidelines for Python code style.
- Type annotations are used throughout the code for better readability.
- Each module and class includes **docstrings**.

---

## Docker Integration

1. **Dockerfile**: Builds the application image with Poetry dependencies.
2. **docker-compose.yml**: Defines multi-service setup (e.g., API and PostgreSQL database).

### Commands

- **Build Docker image**:
   ```bash
   docker-compose up --build
   ```

- **Run application**:
   ```bash
   docker-compose up
   ```

---

This `README.md` serves as a comprehensive guide to setting up the architecture for the FastAPI e-commerce API project, covering all aspects from structure and business rules to configuration and testing.
