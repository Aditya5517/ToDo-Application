# TODO CLI Task Manager

A simple command-line based TODO Task Manager built in Python. This project was developed as part of my internship to strengthen my understanding of Python, modular programming, file handling, exception handling, logging, and command-line applications.

## Features

- Create new tasks
- View all tasks in a table
- Filter tasks by status
- Update tasks by ID or title
- Delete tasks with confirmation
- Archive completed tasks
- View archived tasks separately
- Dashboard with task statistics
- Duplicate task detection
- Input validation and sanitization
- Exception handling
- Logging of user actions
- Interactive menu using Questionary
- Command-line support using argparse

## Project Structure

```text
ToDO CLI/
│
├── main.py           
├── task_manager.py     
├── file_handler.py        
├── validators.py        
├── logs.py          
├── task.json               
├── archive.json         
├── app.log                
├── app_logs.log            
├── README.md
│
├── utils/
│   ├── __init__.py
│   └── helper.py           
│
└── __pycache__/           
``` └── helper.py
```

## Technologies Used

- Python 3
- JSON
- argparse
- questionary
- logging
- tabulate

## Running the Application

### Interactive Mode

```bash
python main.py
```

### Command Line Mode

Create a task
```bash
python main.py create --title "Backend API" --priority High --status Pending
```

View tasks
```bash
python main.py view
```

Update a task
```bash
python main.py update --id 1 --status Completed
```

Delete a task
```bash
python main.py delete --id 1
```

View dashboard
```bash
python main.py dashboard
```

Archive completed tasks
```bash
python main.py archive
```

## Dashboard
The dashboard provides a quick overview of your tasks, including:

- Total Tasks
- Active Tasks
- Archived Tasks
- Pending Tasks
- In Progress Tasks
- Completed Tasks
- Priority Distribution
- Completion Percentage

## Data Storage
The application stores data in JSON files.

- task.json – Active tasks
- archive.json – Archived completed tasks
- app.log – Application logs

## Concepts Practiced
This project helped me practice:

- Modular Programming
- CRUD Operations
- JSON File Handling
- Exception Handling
- Input Validation
- Logging
- Command Line Arguments
- Interactive CLI Development
- Clean Code Organization

## Future Improvements

Some features that can be added in future versions:

- Due dates and reminders
- Task categories and tags
- Search by keyword
- Sorting tasks
- Database integration (SQLite/MySQL)
- User authentication
- Cloud synchronization

## Author

Aditya Mathur

Developed as part of my internship to gain hands-on experience in building a real-world Python CLI application.