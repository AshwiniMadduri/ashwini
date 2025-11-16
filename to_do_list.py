import os

tasks = []

def load_tasks():
    if os.path.exists('tasks.txt'):
        with open('tasks.txt', 'r') as f:
            tasks.extend(f.read().splitlines())

def save_tasks():
    with open('tasks.txt', 'w') as f:
        for task in tasks:
            f.write(task + '\n')

def view_tasks():
    if not tasks:
        print("No tasks in the list.")
    else:
        print("Your To-Do List:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def add_task():
    task = input("Enter the task to add: ").strip()
    if task:
        tasks.append(task)
        save_tasks()
        print("Task added successfully.")
    else:
        print("Task cannot be empty.")

def remove_task():
    view_tasks()
    if tasks:
        try:
            idx = int(input("Enter the task number to remove: ")) - 1
            if 0 <= idx < len(tasks):
                removed = tasks.pop(idx)
                save_tasks()
                print(f"Removed task: {removed}")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")
    else:
        print("No tasks to remove.")

def main():
    load_tasks()
    while True:
        print("\n--- To-Do List Manager ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Quit")
        choice = input("Choose an option (1-4): ").strip()
        if choice == '1':
            view_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            remove_task()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
