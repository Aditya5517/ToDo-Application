import argparse
from file_handler import load_tasks,save_tasks,load_archive,save_archive
from task_manager import create_task, view_tasks, update_task,delete_task,dashboard_statistics,archive_completed_tasks
from validators import valid_priority,valid_status,valid_title
import questionary

# def menu():
#     while True:
#         print("\n=================================")
#         print("        TODO CLI MANAGER")
#         print("=================================")
#         print("1. Create Task")
#         print("2. View Tasks")
#         print("3. Update Task")
#         print("4. Delete Task")
#         print("5. Exit")

#         choice = input("\nChoose an option: ")

#         if choice == "1":
#             create_task()

#         elif choice == "2":
#             view_tasks()

#         elif choice == "3":
#             update_task()

#         elif choice == "4":
#             delete_task()

#         elif choice == "5":
#             print("Thank you for using TODO CLI.")
#             break

#         else:
#             print("Invalid choice. Please select 1-5.")

# if __name__ == "__main__":
#     menu()

def create_parser():
    parser = argparse.ArgumentParser(description="TODO CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command")
    create = subparsers.add_parser("create",help="Create a new task")
    create.add_argument(
        "--title",
        required=True
    )
    create.add_argument(
        "--priority",
        required=True,
        choices=["High", "Medium", "Low"]
    )
    create.add_argument(
        "--status",
        required=True,
        choices=[
            "Pending",
            "In Progress",
            "Completed"
        ]
    )

    view = subparsers.add_parser(
        "view",
        help="View tasks"
    )

    view.add_argument(
        "--status",
        choices=[
            "Pending",
            "In Progress",
            "Completed"
        ]
    )
    delete = subparsers.add_parser(
        "delete",
        help="Delete a task"
    )

    delete.add_argument(
        "--id",
        type=int,
        required=True
    )
    update = subparsers.add_parser(
        "update",
        help="Update task"
    )

    update.add_argument(
        "--id",
        type=int,
        required=True
    )

    update.add_argument("--title")

    update.add_argument(
        "--priority",
        choices=["High", "Medium", "Low"]
    )

    update.add_argument(
        "--status",
        choices=[
            "Pending",
            "In Progress",
            "Completed"
        ]
    )

    subparsers.add_parser(
        "dashboard",
        help="Show dashboard"
    )

    subparsers.add_parser(
        "archive",
        help="Archive completed tasks"
    )
    return parser

parser = create_parser()
args = parser.parse_args()


def menu():
    while True:
        choice = questionary.select(
            "TODO CLI Manager",
            choices=[
                "Create Task",
                "View Tasks",
                "Update Task",
                "Delete Task",
                "Dashboard",
                "Archive completed tasks",
                "Exit"
            ]
        ).ask()

        if choice == "Create Task":
            create_task()

        elif choice == "View Tasks":
            view_tasks()

        elif choice == "Update Task":
            update_task()

        elif choice == "Delete Task":
            delete_task()

        elif choice == "Dashboard":
            dashboard_statistics()

        elif choice =="Archive completed tasks":
            archive_completed_tasks()

        elif choice == "Exit":
            print("Thank you for using TODO CLI Manager.")
            break

if __name__ == "__main__":

    if args.command is None:
        menu()
    elif args.command == "create":
        create_task(
            args.title,
            args.priority,
            args.status
        )
    elif args.command == "view":
        view_tasks(args.status)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "update":
        update_task(
            args.id,
            args.title,
            args.priority,
            args.status
        )
    elif args.command == "dashboard":
        dashboard_statistics()
    elif args.command == "archive":
        archive_completed_tasks()