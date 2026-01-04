import json
from datetime import datetime, date

# File where tasks will be stored
TASK_FILE = "tasks.json"

# Loading existing tasks from file
def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file is missing or corrupted

# Save tasks to file
def save_tasks():
    with open(TASK_FILE, "w") as file:
        json.dump(to_do_list, file, indent=4, default=str)  # Convert datetime to string

# Initialize task list
to_do_list = load_tasks()


def add_task():
    """Add a new task with optional due date."""
    task = input('Please input the name of the task: ').strip()
    description = input('Please input the description of the task: ').strip()
    optional_due_date = input('Please input optional due date (format: YYYY-MM-DD) or leave blank: ').strip()

    task_data = {
        'Task name': task.lower(),
        'Description': description,
        'Status': 'Pending'
    }

    if optional_due_date:
        try:
            task_data['Due Date'] = datetime.strptime(optional_due_date, '%Y-%m-%d').date().isoformat()
        except ValueError:
            print('Invalid date format! Task added without due date.')

    to_do_list.append(task_data)
    save_tasks()  # Save after adding a task


def view_all_tasks():
    """Display all tasks with status and due date."""
    if not to_do_list:
        print('\n📌 List has no tasks yet!')
        return

    print("\n📋 TO-DO LIST 📋\n" + "=" * 30)
    pending = 0
    completed = 0
    today = date.today()

    for index, item in enumerate(to_do_list, start=1):
        print(f'\n🔹 {index}. Task name: {item["Task name"]}')
        print(f' 📖 Description: {item["Description"]}')
        print(f' 📌 Status: {item["Status"]}')

        if 'Due Date' in item:
            due_date = date.fromisoformat(item["Due Date"])
            print(f' 📅 Due Date: {due_date}')

            if due_date < today:
                print('❌ Overdue!')
            elif due_date == today:
                print('⚠️ Due today!')
            else:
                print('🟢 On track!')

        if item['Status'] == 'Pending':
            pending += 1
        else:
            completed += 1

    print(f'\n🔵 You have {pending} Pending task(s).')
    print(f'🟢 You have completed {completed} task(s).')


def mark_task_completed(task_name):
    """Mark a task as completed."""
    for task in to_do_list:
        if task_name.lower() in task['Task name']:
            task['Status'] = 'Completed'
            save_tasks()  # Save changes
            print(f'Task: {task_name} marked as completed!')
            return
    print('Task name not found!')


def delete_task(task_name):
    """Delete a task by name."""
    global to_do_list
    original_length = len(to_do_list)
    to_do_list = [task for task in to_do_list if task_name.lower() not in task['Task name']]

    if len(to_do_list) < original_length:
        save_tasks()  # Save after deletion
        print(f'Task: {task_name} was removed!')
    else:
        print('Task not found!')


def remove_completed_tasks():
    """Remove all completed tasks from the list."""
    global to_do_list
    to_do_list = [task for task in to_do_list if task['Status'] != 'Completed']
    save_tasks()  # Save after removing tasks
    print('\n✅ All completed tasks removed!')


def to_do_list_app():
    """Main loop for the to-do list program."""
    while True:
        print('\nOptions:')
        print('1. Add a task')
        print('2. View all tasks')
        print('3. Mark a task as completed')
        print('4. Delete a task')
        print('5. Remove all completed tasks')
        print('6. Exit the app')

        choice = input('Choose an option (1-6): ').strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_all_tasks()
        elif choice == '3':
            task_name = input('Enter the task name to mark as completed: ').strip()
            mark_task_completed(task_name)
        elif choice == '4':
            task_name = input('Enter the task name to delete: ').strip()
            delete_task(task_name)
        elif choice == '5':
            remove_completed_tasks()
        elif choice == '6':
            print('Goodbye!')
            break
        else:
            print('❌ Invalid choice! Please enter a number between 1 and 6.')

# Start the app
to_do_list_app()

