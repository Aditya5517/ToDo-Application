# ToDo Application

A Python-based ToDo management system developed as part of a modular application and backend learning project.

The repository contains both a **CLI-based ToDo application** and a **FastAPI backend application**, along with supporting Python learning material and documentation.

---

## Repository Structure

```text
Repository/
│
├── DOCS/
│   └── Project documentation and related files
│
├── PYTHON/
│   └── Python learning programs and practice files
│
├── ToDO CLI/
│   └── Command-line ToDo application
│
├── ToDo Application/
│   └── FastAPI-based backend application
│
└── README.md
```

---

# 1. ToDO CLI

The **ToDO CLI** is a command-line task management application built using Python.

It allows users to manage tasks directly from the terminal.

### Features

* Create tasks
* View tasks
* Update tasks
* Delete tasks
* Filter tasks by status
* Validate user input
* Sanitize task information
* Automatically generate task IDs
* Store data in a JSON file
* Handle file-related exceptions
* Log application activities
* Display tasks in a formatted table

### Main Components

```text
ToDO CLI/
├── utils/
├── services/
├── file_handler.py
├── logs.py
├── main.py
├── MOCK_DATA.json
└── activity.log
```

### Run the CLI

Navigate to the project directory:

```bash
cd "ToDO CLI"
```

Install required dependencies:

```bash
pip install questionary tabulate
```

Run the application:

```bash
python main.py
```

---

# 2. ToDo Application

The **ToDo Application** is the backend version of the ToDo project built using **FastAPI**.

It exposes task management functionality through REST API endpoints.

### Features

* Create tasks through REST APIs
* Retrieve all tasks
* Retrieve a task by ID
* Update existing tasks
* Delete tasks
* Search/filter tasks
* Request validation using Pydantic
* Error handling
* JSON-based data persistence
* Modular project structure
* Activity logging
* Interactive Swagger API documentation

### Project Structure

```text
ToDo Application/
│
├── Backend/
│   └── src/
│       ├── routes/
│       ├── services/
│       ├── utils/
│       ├── main.py
│       ├── file_handler.py
│       ├── logs.py
│       └── MOCK_DATA.json
│
└── ...
```

> Update the structure above if your current `ToDo Application` folder has a different arrangement.

---

## REST API

The FastAPI backend provides endpoints for task management.

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/tasks`           | Get all tasks       |
| GET    | `/tasks/{task_id}` | Get a task by ID    |
| POST   | `/tasks`           | Create a new task   |
| PUT    | `/tasks/{task_id}` | Update a task       |
| DELETE | `/tasks/{task_id}` | Delete a task       |
| GET    | `/tasks/search`    | Search/filter tasks |

### Example Request

```json
{
  "title": "Learn FastAPI",
  "priority": "High",
  "status": "Pending"
}
```

### Example Response

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "priority": "High",
  "status": "Pending"
}
```

---

## Running the FastAPI Backend

Navigate to the backend source directory:

```bash
cd "ToDo Application/Backend/src"
```

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Architecture

The backend follows a modular architecture:

```text
Client
  │
  ▼
Routes
  │
  ▼
Services
  │
  ▼
File Handler
  │
  ▼
MOCK_DATA.json
```

### Routes

Handles incoming HTTP requests and returns API responses.

### Services

Contains the application's business logic for task operations.

### Utils

Contains reusable validation and helper functions.

### File Handler

Handles loading and saving task data in JSON format.

### Logging

Records important application activities and errors in `activity.log`.

---

## Data Storage

The application uses a local JSON file instead of an external database.

Example:

```json
[
  {
    "id": 1,
    "title": "Complete Python assignment",
    "priority": "High",
    "status": "Pending"
  },
  {
    "id": 2,
    "title": "Study FastAPI",
    "priority": "Medium",
    "status": "Completed"
  }
]
```

This makes the project simple to run without requiring database configuration.

---

## Validation

The application validates task information before processing it.

Validation includes:

* Required task title
* Valid task priority
* Valid task status
* Valid task ID
* Input sanitization
* Handling invalid input

The FastAPI backend additionally uses **Pydantic** models for request validation.

---

## Logging

Application activities are recorded in:

```text
activity.log
```

Examples of logged operations include:

```text
[2026-08-12 10:30:15] INFO - Created task
[2026-08-12 10:35:20] INFO - Viewed task list
[2026-08-12 10:40:12] INFO - Updated task ID: 2
[2026-08-12 10:45:30] WARNING - Task ID 10 not found
```

---

## Technologies Used

* **Python 3.12**
* **FastAPI**
* **Pydantic**
* **Uvicorn**
* **Questionary**
* **Tabulate**
* **JSON**
* **Python Logging**

---

## Learning Objectives

This project was developed to practice:

* Python programming
* Modular project structure
* Separation of concerns
* Input validation
* Exception handling
* File handling
* JSON data persistence
* Logging
* REST API development
* FastAPI
* Pydantic
* API routing
* Service-layer architecture
* Git and GitHub workflow

---

## Future Improvements

* Database integration
* User authentication
* JWT authorization
* Task due dates
* Task categories
* Pagination for API responses
* Automated unit and API testing
* Docker support
* CI/CD integration
* Frontend application

---


