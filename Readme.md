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
│   ├── domain/                # Core business logic (Entities, Value Objects, and Domain Services)
│   │   ├── entities/          # Entities to represent core domain objects
│   │   │   ├── base_entity.py
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── reservation.py
│   │   │   ├── sale.py
│   │   │   └── __init__.py
│   │   ├── values/            # Value Objects representing specific domain values
│   │   │   ├── base_value_object.py
│   │   │   ├── price.py
│   │   │   ├── quantity.py
│   │   │   ├── discount.py
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
│   │   ├── converters/
│   │   │   ├── product_converters.py       
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
│   └── __init__.py
│
├── tests/
│   │── conftest.py
│   │── pytest.ini
│   │── test_container.py
│   │── domain/
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── test_product_service.py
│   │   │   ├── test_category_service.py
│   │   │   ├── test_reservation_service.py
│   │   │   └── test_sale_service.py
│   │   └── __init__.py
│   │── presentation/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── test_products.py
│   │   │       ├── test_categories.py
│   │   │       ├── test_reservations.py
│   │   │       ├── test_sales.py
│   │   │       └── __init__.py
│   │   └── __init__.py
│   └── __init__.py
└─
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

# Products

- **Retrieve Product List**
  - `GET /api/products/`
  - **Description:** Returns a list of all available products. Can be filtered by category.
  - **Query Parameters:**
    - `category_id` (optional) — UUID of the category to filter products.

- **Retrieve Product Details**
  - `GET /api/products/{product_id}/`
  - **Description:** Returns information about a specific product.
  - **Path Parameters:**
    - `product_id` — UUID of the product.

- **Add New Product**
  - `POST /api/products/`
  - **Description:** Creates a new product.
  - **Request Body (JSON):**
    - `name` — name of the product.
    - `category_id` — UUID of the category.
    - `price` — price of the product.
    - `stock` — quantity in stock.

- **Update Product**
  - `PUT /api/products/{product_id}/`
  - **Description:** Updates information about a product (price, discount, stock availability).
  - **Path Parameters:**
    - `product_id` — UUID of the product.
  - **Request Body (JSON):**
    - Any fields of the product that need updating (`name`, `price`, `stock`, `discount`).

- **Delete Product**
  - `DELETE /api/products/{product_id}/`
  - **Description:** Deletes a product from the database.
  - **Path Parameters:**
    - `product_id` — UUID of the product.

# Reservations

- **Create Reservation**
  - `POST /api/reservations/`
  - **Description:** Reserves a specific quantity of a product.
  - **Request Body (JSON):**
    - `product_id` — UUID of the product.
    - `quantity` — quantity to reserve.

- **Cancel Reservation**
  - `DELETE /api/reservations/{reservation_id}/`
  - **Description:** Cancels a product reservation.
  - **Path Parameters:**
    - `reservation_id` — UUID of the reservation.

# Sales

- **Register Sale**
  - `POST /api/sales/`
  - **Description:** Registers the sale of a product.
  - **Request Body (JSON):**
    - `product_id` — UUID of the product.
    - `quantity` — quantity of the product sold.

- **Retrieve Sales Report**
  - `GET /api/sales/`
  - **Description:** Returns a report of sold products.
  - **Optional Query Parameters:**
    - `start_date` — start date of the period.
    - `end_date` — end date of the period.
    - `category_id` — UUID of the category for filtering.

# Categories

- **Retrieve Category List**
  - `GET /api/categories/`
  - **Description:** Returns a list of all categories.

- **Add New Category**
  - `POST /api/categories/`
  - **Description:** Creates a new category.
  - **Request Body (JSON):**
    - `name` — name of the category.
    - `parent_category_id` (optional) — UUID of the parent category.

# Promotions

- **Set Discount on Product**
  - `PUT /api/products/{product_id}/promotion`
  - **Description:** Sets a discount on a product.
  - **Path Parameters:**
    - `product_id` — UUID of the product.
  - **Request Body (JSON):**
    - `discount_percentage` — discount percentage.


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


### Test Suite Overview

The project contains a comprehensive suite of tests covering both service-level and API-level operations for managing the various entities, such as products, categories, reservations, and sales. The tests are designed to ensure the proper functioning of the core business logic and API endpoints of the application. The tests are structured to verify CRUD operations, data validation, and error handling across different components of the system.

The tests are divided into two main categories:
1. **Domain Service Tests**: These tests validate the core business logic for each of the entities.
2. **API Endpoint Tests**: These tests cover the REST API operations for managing the entities via HTTP requests.

Below is an overview of each test file and the types of scenarios covered.

#### Domain Service Tests

The tests for the domain services are located under the `tests/domain/services/` directory, and they validate the core business logic for the entities using Python `pytest`. Here is a detailed description of the different test files:

#### 1. `test_category_service.py`
- **`test_create_category`**: Checks if a new category can be successfully created, ensuring that the created category matches the input data.
- **`test_get_category_by_id`**: Verifies that a category can be correctly fetched by its unique identifier.
- **`test_get_nonexistent_category`**: Ensures that an attempt to retrieve a non-existent category raises a `CategoryNotFoundException`.
- **`test_get_all_categories`**: Confirms that fetching all categories returns a list of all created categories.

#### 2. `test_product_service.py`
- **`test_create_product`**: Verifies that a new product can be successfully created, ensuring it matches the expected DTO representation.
- **`test_get_available_products`**: Ensures that retrieving available products filtered by a category returns all products with stock greater than zero.
- **`test_apply_discount`**: Verifies that applying a valid discount correctly updates the product's price and discount.
- **`test_apply_invalid_discount`**: Confirms that applying an invalid discount (e.g., more than 100%) raises an `InvalidDiscountException`.
- **`test_update_price_nonexistent_product`**: Validates that attempting to update the price of a non-existent product results in a `ProductNotFoundException`.
- **`test_reserve_product_insufficient_stock`**: Ensures that attempting to reserve a quantity of product exceeding available stock raises an `InsufficientStockException`.
- **`test_sell_product_insufficient_stock`**: Verifies that selling a quantity exceeding stock raises an `InsufficientStockException`.

#### 3. `test_reservation_service.py`
- **`test_create_reservation`**: Verifies that a new reservation can be successfully created with the specified product ID and quantity, and that the status is set to "reserved".
- **`test_cancel_reservation`**: Ensures that an existing reservation can be successfully canceled and the status is updated to "cancelled".
- **`test_get_nonexistent_reservation`**: Confirms that retrieving a non-existent reservation raises a `ReservationNotFoundException`.

#### 4. `test_sale_service.py`
- **`test_record_sale`**: Checks that a sale can be successfully recorded with the specified product ID and quantity.
- **`test_get_sales_between_dates`**: Ensures that retrieving sales within a specified date range returns all relevant sales records.
- **`test_get_nonexistent_sale`**: Validates that attempting to retrieve a sale that does not exist raises a `SaleNotFoundException`.

### API Endpoint Tests

The API endpoint tests are located under `tests/presentation/api/v1/` and use `httpx.AsyncClient` for making requests to the FastAPI application. These tests verify the HTTP responses and ensure the endpoints are working correctly.

#### 1. `test_categories.py`
- **`test_create_category`**: Tests the creation of a new category with a randomly generated UUID as its parent category ID.
- **`test_create_category_with_parent`**: Verifies the creation of a sub-category linked to a specific parent category.
- **`test_update_category`**: Tests updating a category's name to ensure partial updates are handled correctly.
- **`test_delete_category`**: Verifies that a category can be deleted and that it cannot be retrieved afterward.

#### 2. `test_products.py`
- **`test_create_product`**: Tests the creation of a new product, verifying the response contains correct product details.
- **`test_get_products`**: Verifies that the API can successfully return a list of products.
- **`test_get_product_by_id`**: Ensures that a specific product can be retrieved by its ID.
- **`test_update_product`**: Confirms that a product's details can be successfully updated.
- **`test_delete_product`**: Validates that a product can be deleted and that subsequent retrieval returns a 404 status.

#### 3. `test_reservations.py`
- **`test_create_reservation`**: Tests the creation of a reservation, ensuring the reservation details are correct.
- **`test_cancel_reservation`**: Verifies that an existing reservation can be successfully canceled.

#### 4. `test_sales.py`
- **`test_register_sale`**: Tests the registration of a new sale, ensuring the correct product ID and quantity are recorded.
- **`test_get_sales`**: Ensures that sales can be fetched within a specified date range.

### Test Summary

- **Number of Tests**: The suite contains a total of **31 tests**, all of which pass successfully.

All tests have passed successfully, confirming the robustness of the implemented features and the reliability of both service-level and API-level operations.

