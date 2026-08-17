from services.file_handler import load_tasks, save_tasks,load_archive,save_archive
from src.utils import helper 
from src.utils.validators import valid_priority,valid_status,valid_title
from src.utils.logs import logger
import questionary
from tabulate import tabulate

def create_task(title=None, priority=None, status=None):
    tasks = load_tasks()

    # =========================
    # TITLE
    # =========================
    if title is None:

        while True:
            title = questionary.text(
                "Enter Task Title (type BACK to return):"
            ).ask()

            if title is None or helper.is_back(title):
                print("\nReturning to main menu...")
                return

            title = helper.sanitize_string(title)

            if not valid_title(title):
                print("\nPlease enter a valid task title.")
                print("Title must contain at least one letter.\n")
                continue

            if helper.task_exists(tasks, title):
                print("\nTask already exists.")
                print("Please enter a different title.\n")
                continue

            break

    else:
        title = helper.sanitize_string(title)

        if not valid_title(title):
            print("Please enter a valid task title.")
            return

        if helper.task_exists(tasks, title):
            print("Task already exists.")
            return

    # =========================
    # PRIORITY
    # =========================
    if priority is None:

        while True:
            priority = questionary.text(
                "Enter Priority (High/Medium/Low) "
                "(type BACK to return):"
            ).ask()

            if priority is None or helper.is_back(priority):
                print("\nReturning to main menu...")
                return

            priority = helper.normalize_priority(priority)

            if not valid_priority(priority):
                print("\nPlease enter High, Medium or Low.\n")
                continue

            break

    else:
        priority = helper.normalize_priority(priority)

        if not valid_priority(priority):
            print("Please enter High, Medium or Low.")
            return

    # =========================
    # STATUS
    # =========================
    if status is None:

        while True:
            status = questionary.text(
                "Enter Status (Pending/In Progress/Completed) "
                "(type BACK to return):"
            ).ask()

            if status is None or helper.is_back(status):
                print("\nReturning to main menu...")
                return

            status = helper.normalize_status(status)

            if not valid_status(status):
                print(
                    "\nPlease enter one of:"
                    "\n- Pending"
                    "\n- In Progress"
                    "\n- Completed\n"
                )
                continue

            break

    else:
        status = helper.normalize_status(status)

        if not valid_status(status):
            print("Please enter Pending, In Progress or Completed.")
            return

    # =========================
    # CREATE TASK
    # =========================
    task_id = helper.generate_id(tasks)

    new_task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "status": status
    }

    print("\n========== TASK SUMMARY ==========\n")
    helper.print_task(new_task)

    confirm = questionary.confirm(
        "Create this task?"
    ).ask()

    if not confirm:
        logger.info("Task creation cancelled by user.")
        print("\nTask creation cancelled.")
        return

    tasks.append(new_task)
    save_tasks(tasks)

    logger.info(
        f"Task Created | ID={task_id} | Title='{title}'"
    )

    print("\nTask created successfully!")
    print(f"Task ID: {task_id}")


def view_tasks(status=None):
    tasks = load_tasks()
    logger.info("Viewed task list.")

    if not tasks:
        logger.warning("View Tasks requested but no tasks exist.")
        print("No existing tasks!")
        return

    while True:

        choice = questionary.select(
            "View Tasks",
            choices=[
                "View All Tasks",
                "Pending Tasks",
                "In Progress Tasks",
                "Completed Tasks",
                "Search by Task ID",
                "Back"
            ]
        ).ask()

        if choice == "View All Tasks":
            logger.info("Viewed all tasks.")
            filtered_tasks = tasks

        elif choice == "Pending Tasks":
            logger.info("Viewed Pending tasks.")
            filtered_tasks = [
                task for task in tasks
                if task["status"] == "Pending"
            ]

        elif choice == "In Progress Tasks":
            logger.info("Viewed In Progress tasks.")
            filtered_tasks = [
                task for task in tasks
                if task["status"] == "In Progress"
            ]

        elif choice == "Completed Tasks":
            logger.info("Viewed Completed tasks.")
            filtered_tasks = [
                task for task in tasks
                if task["status"] == "Completed"
            ]

        elif choice == "Search by Task ID":

            task_id = helper.safe_int(input("Enter Task ID: "))

            if task_id is None:
                logger.warning("User entered an invalid Task ID while searching.")
                print("Please enter a valid Task ID.")
                continue

            logger.info(f"Viewed Task | ID={task_id}")
            task = helper.find_task_by_id(tasks, task_id)

            if task is None:
                logger.warning(f"Task search failed. Task ID={task_id} not found.")
                print("Task not found.")
                continue
            logger.info(f"Viewed Task | ID={task_id}")
            filtered_tasks = [task]

        elif choice == "Back":
            logger.info("Exited View Tasks menu.")
            return
        if not filtered_tasks:
            logger.info(f"No tasks found for filter: {choice}")
            print("\nNo matching tasks found.\n")
            continue
        logger.info(f"Displayed {len(filtered_tasks)} task(s) for option '{choice}'.")
        print("\n========== TASK LIST ==========\n")
        table = []

        for task in filtered_tasks:
            table.append([
                task["id"],
                task["title"],
                task["priority"],
                task["status"]
            ])

        print(
            tabulate(
                table,
                headers=["ID", "Title", "Priority", "Status"],
                tablefmt="grid"
            )
        )
        input("\nPress Enter to continue...")


def view_archive(status=None):
    archived_tasks = load_archive()

    if not archived_tasks:
        print("\nNo archived tasks found.")
        return

    table = []

    for task in archived_tasks:
        table.append([
            task["id"],
            task["title"],
            task["priority"],
            task["status"]
        ])

    print("\n========== ARCHIVED TASKS ==========\n")

    print(tabulate(
        table,
        headers=["ID", "Title", "Priority", "Status"],
        tablefmt="grid"
    ))

    input("\nPress Enter to continue...")


def update_task(task_id=None, title=None, priority=None, status=None):
    
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    # =========================
    # SEARCH TASK
    # =========================
    while True:

        search_by = questionary.select(
            "How would you like to search the task?",
            choices=[
                "Search by ID",
                "Search by Title",
                "Back"
            ]
        ).ask()

        if search_by == "Back":
            print("\nReturning to main menu...")
            return

        # -------------------------
        # SEARCH BY ID
        # -------------------------
        if search_by == "Search by ID":

            while True:

                value = questionary.text(
                    "Enter Task ID (type BACK to return):"
                ).ask()

                if value is None or helper.is_back(value):
                    print("\nReturning to main menu...")
                    return

                task_id = helper.safe_int(value)

                if task_id is None:
                    print("\nPlease enter a valid numeric Task ID.")
                    continue

                task = helper.find_task_by_id(tasks, task_id)

                if task is None:
                    print(
                        "\nTask with this ID does not exist."
                    )
                    print(
                        "Please enter another Task ID."
                    )
                    continue

                break

        # -------------------------
        # SEARCH BY TITLE
        # -------------------------
        else:

            while True:

                title = questionary.text(
                    "Enter Task Title (type BACK to return):"
                ).ask()

                if title is None or helper.is_back(title):
                    print("\nReturning to main menu...")
                    return

                title = helper.sanitize_string(title)

                if not title:
                    print("\nPlease enter a valid task title.")
                    continue

                task = helper.find_task_by_title(
                    tasks,
                    title
                )

                if task is None:
                    print(
                        "\nTask with this title does not exist."
                    )
                    print(
                        "Please enter another title."
                    )
                    continue

                break

        break

    # =========================
    # CURRENT DETAILS
    # =========================

    print("\n========== CURRENT TASK ==========\n")
    helper.print_task(task)

    # =========================
    # SELECT FIELD
    # =========================

    field = questionary.select(
        "What would you like to update?",
        choices=[
            "Title",
            "Priority",
            "Status",
            "Complete Task",
            "Back"
        ]
    ).ask()

    if field == "Back":
        print("\nReturning to main menu...")
        return

    # =========================
    # UPDATE TITLE
    # =========================

    if field == "Title":

        print(f"\nCurrent Title: {task['title']}")

        while True:

            new_title = questionary.text(
                "Enter New Title (type BACK to return):"
            ).ask()

            if new_title is None or helper.is_back(new_title):
                print("\nUpdate cancelled.")
                return

            new_title = helper.sanitize_string(new_title)

            if not valid_title(new_title):
                print("\nPlease enter a valid task title.")
                continue

            # Don't consider the current task itself a duplicate
            duplicate = False

            for existing_task in tasks:
                if (
                    existing_task["id"] != task["id"]
                    and helper.sanitize_string(
                        existing_task["title"]
                    ).lower() == new_title.lower()
                ):
                    duplicate = True
                    break

            if duplicate:
                print("\nTask with this title already exists.")
                continue

            task["title"] = new_title
            break

    # =========================
    # UPDATE PRIORITY
    # =========================

    elif field == "Priority":

        print(f"\nCurrent Priority: {task['priority']}")

        while True:

            new_priority = questionary.text(
                "Enter New Priority (High/Medium/Low) "
                "(type BACK to return):"
            ).ask()

            if new_priority is None or helper.is_back(new_priority):
                print("\nUpdate cancelled.")
                return

            new_priority = helper.normalize_priority(
                new_priority
            )

            if not valid_priority(new_priority):
                print(
                    "\nPlease enter:"
                    "\n- High"
                    "\n- Medium"
                    "\n- Low\n"
                )
                continue

            task["priority"] = new_priority
            break

    # =========================
    # UPDATE STATUS
    # =========================

    elif field == "Status":

        print(f"\nCurrent Status: {task['status']}")

        while True:

            new_status = questionary.text(
                "Enter New Status "
                "(Pending/In Progress/Completed) "
                "(type BACK to return):"
            ).ask()

            if new_status is None or helper.is_back(new_status):
                print("\nUpdate cancelled.")
                return

            new_status = helper.normalize_status(
                new_status
            )

            if not valid_status(new_status):
                print(
                    "\nInvalid status."
                    "\nPlease enter:"
                    "\n- Pending"
                    "\n- In Progress"
                    "\n- Completed\n"
                )
                continue

            task["status"] = new_status
            break

    # =========================
    # COMPLETE TASK
    # =========================

    elif field == "Complete Task":

        print("\nEnter new details.")
        print("Type BACK at any point to cancel.\n")

        # TITLE
        while True:

            new_title = questionary.text(
                f"Title ({task['title']}):"
            ).ask()

            if new_title is None or helper.is_back(new_title):
                print("\nUpdate cancelled.")
                return

            new_title = helper.sanitize_string(new_title)

            if not valid_title(new_title):
                print("\nPlease enter a valid title.")
                continue

            task["title"] = new_title
            break

        # PRIORITY
        while True:

            new_priority = questionary.text(
                f"Priority ({task['priority']}):"
            ).ask()

            if new_priority is None or helper.is_back(new_priority):
                print("\nUpdate cancelled.")
                return

            new_priority = helper.normalize_priority(
                new_priority
            )

            if not valid_priority(new_priority):
                print(
                    "\nPlease enter High, Medium or Low."
                )
                continue

            task["priority"] = new_priority
            break

        # STATUS
        while True:

            new_status = questionary.text(
                f"Status ({task['status']}):"
            ).ask()

            if new_status is None or helper.is_back(new_status):
                print("\nUpdate cancelled.")
                return

            new_status = helper.normalize_status(
                new_status
            )

            if not valid_status(new_status):
                print(
                    "\nPlease enter:"
                    "\n- Pending"
                    "\n- In Progress"
                    "\n- Completed"
                )
                continue

            task["status"] = new_status
            break

    # =========================
    # REVIEW CHANGES
    # =========================

    print("\n========== REVIEW CHANGES ==========\n")
    helper.print_task(task)

    confirm = questionary.confirm(
        "Save these changes?"
    ).ask()

    if not confirm:
        logger.info(
            f"Update cancelled | ID={task['id']}"
        )
        print("\nUpdate cancelled.")
        return

    save_tasks(tasks)

    logger.info(
        f"Task Updated | ID={task['id']}"
    )

    print("\nTask updated successfully!")


def delete_task(task_id=None):
    tasks = load_tasks()
    task_id = helper.safe_int(questionary.text("Enter Task ID:").ask())
    if task_id is None:
        print("Task ID must be a number.")
        return
    task = helper.find_task_by_id(tasks, task_id)
    if task is None:
        print("Task not found.")
        logger.warning(f"Delete failed | Task ID={task_id} not found.")
        return
    print("\nTask to Delete\n")
    helper.print_task(task)
    confirm = questionary.confirm("Are you sure you want to delete this task?").ask()
    if not confirm:
        print("Deletion cancelled.")
        logger.info(f"Deletion cancelled | ID={task['id']}")
        return
    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted successfully!")
    logger.info(f"Task Deleted | ID={task['id']}")


def dashboard_statistics():
    tasks = load_tasks()
    archived_tasks = load_archive()

    logger.info("Dashboard viewed.")

    # Total tasks
    total_active = len(tasks)
    total_archived = len(archived_tasks)
    total = total_active + total_archived

    if total == 0:
        print("No tasks available.")
        return

    # Status Counters
    pending = 0
    progress = 0
    completed = 0

    # Priority Counters
    high = 0
    medium = 0
    low = 0

    # Active Tasks
    for task in tasks:

        if task["status"] == "Pending":
            pending += 1

        elif task["status"] == "In Progress":
            progress += 1

        if task["priority"] == "High":
            high += 1

        elif task["priority"] == "Medium":
            medium += 1

        elif task["priority"] == "Low":
            low += 1

    # Archived Tasks
    for task in archived_tasks:

        if task["status"] == "Completed":
            completed += 1

        # Count archived task priorities as well
        if task["priority"] == "High":
            high += 1

        elif task["priority"] == "Medium":
            medium += 1

        elif task["priority"] == "Low":
            low += 1

    completion_rate = (completed / total) * 100

    print("\n========== DASHBOARD ==========\n")

    print(f"Total Tasks         : {total}")
    print(f"Active Tasks        : {total_active}")
    print(f"Archived Tasks      : {total_archived}")
    print()

    print(f"Pending             : {pending}")
    print(f"In Progress         : {progress}")
    print(f"Completed           : {completed}")
    print()

    print(f"High Priority       : {high}")
    print(f"Medium Priority     : {medium}")
    print(f"Low Priority        : {low}")
    print()

    print(f"Completion Rate     : {completion_rate:.2f}%")

    print("\n===============================\n")

def archive_completed_tasks():
    tasks = load_tasks()
    archive = load_archive()
    completed_tasks = []
    remaining_tasks = []
    for task in tasks:
        if task["status"] == "Completed":
            completed_tasks.append(task)
        else:
            remaining_tasks.append(task)
    if not completed_tasks:
        print("No completed tasks to archive.")
        return
    print("\nCompleted Tasks\n")
    for task in completed_tasks:
        helper.print_task(task)
    confirm = questionary.confirm(f"Archive {len(completed_tasks)} completed task(s)?").ask()
    if not confirm:
        print("Archive cancelled.")
        return
    archive.extend(completed_tasks)
    save_archive(archive)
    logger.info(f"Archived {len(completed_tasks)} completed task(s).")
    save_tasks(remaining_tasks)
    print(f"{len(completed_tasks)} task(s) archived successfully.")