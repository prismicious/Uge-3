# CerealAPI Project

This project provides a RESTful API for managing a collection of cereals. It includes functionalities to create, read, update, and delete cereal records, as well as to filter cereals based on specific criteria. The application is built using Python's Flask framework and interacts with an SQLite database.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **CRUD Operations**: Create, read, update, and delete cereal records.
- **Filtering**: Filter cereals based on query parameters.
- **Concurrent Execution**: The application runs the Flask API and a test driver concurrently using multithreading.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/prismicious/Uge-3.git
   cd cereal-api
   ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
## Usage

### Running the Application

The application is designed to run both the Flask API and a test driver concurrently. The `Main` class initializes the necessary components and starts the Flask server in a separate thread to allow the driver to perform API tests.

To start the application:

```bash
python main.py
```
## API Documentation

### Authorization

The API utilizes password authentication with bcrypt hashing.

- **GET** requests do not require authentication.
- **POST**, **INSERT**, and **DELETE** requests require authentication.

### Endpoints

| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| GET    | `/cereals`          | Retrieve all cereals                      |
| GET    | `/cereals/<id>`     | Retrieve a cereal by ID                   |
| GET    | `/cereals?key=value` | Filter cereals based on query parameters |
| POST   | `/cereals`          | Create a new cereal                       |
| POST   | `/cereals/<id>`     | Update an existing cereal by ID           |
| DELETE | `/cereals/<id>`     | Delete a cereal by ID                     |

*Note: Replace `<id>` with the actual cereal ID and `key=value` with your filter criteria.*

## Testing

The `Driver` class contains methods to test the API endpoints. It performs the following sequence of tests:

1. Retrieve a cereal by ID.
2. Retrieve all cereals.
3. Filter cereals based on manufacturer and shelf.
4. Delete a cereal by ID.
5. Create a new cereal.
6. Update an existing cereal by ID.
7. Attempt to retrieve a non-existent cereal by ID.

These tests run automatically when the application is started.
