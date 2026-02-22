#!/usr/bin/env python3

import argparse
import json
import os
import sys


def load_tasks():
    """Load tasks from tasks.json file."""
    try:
        if not os.path.exists("tasks.json"):
            return []
        
        with open("tasks.json", "r") as file:
            return json.load(file)
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON in tasks.json", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading tasks.json: {e}", file=sys.stderr)
        return []


def save_tasks(tasks):
    """Save tasks to tasks.json file."""
    try:
        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}", file=sys.stderr)
        return False


def add_task(description):
    """Add a new task with the given description."""
    if not description or not description.strip():
        print("Error: Task description cannot be empty", file=sys.stderr)
        return
    
    tasks = load_tasks()
    new_id = len(tasks) + 1 if tasks else 1
    
    new_task = {
        "id": new_id,
        "description": description.strip(),
        "completed": False
    }
    
    tasks.append(new_task)
    if save_tasks(tasks):
        print(f"Task added: {new_id}. {description.strip()}")


def list_tasks():
    """Display all tasks."""
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found.")
        return
    
    print("\nTasks:")
    print("-" * 50)
    
    for task in tasks:
        status = "✓" if task["completed"] else "○"
        print(f"{task['id']}. [{status}] {task['description']}")
    
    print()


def complete_task(task_id):
    """Mark task as completed."""
    if task_id <= 0:
        print("Error: Task ID must be a positive integer", file=sys.stderr)
        return
    
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            if save_tasks(tasks):
                print(f"Task {task_id} marked as completed.")
            return
    
    print(f"Task with ID {task_id} not found.", file=sys.stderr)


def delete_task(task_id):
    """Delete a task."""
    if task_id <= 0:
        print("Error: Task ID must be a positive integer", file=sys.stderr)
        return
    
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            # Re-index tasks
            for j, remaining_task in enumerate(tasks, 1):
                remaining_task["id"] = j
            if save_tasks(tasks):
                print(f"Task {task_id} deleted.")
            return
    
    print(f"Task with ID {task_id} not found.", file=sys.stderr)


def main():
    """Main entry point for the CLI application."""
    try:
        parser = argparse.ArgumentParser(description="CLI Task Manager")
        subparsers = parser.add_subparsers(dest='command')
        
        # Add task command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('description', help='Task description')
        
        # List tasks command
        subparsers.add_parser('list', help='List all tasks')
        
        # Complete task command
        complete_parser = subparsers.add_parser('complete', help='Mark task as completed')
        complete_parser.add_argument('id', type=int, help='Task ID')
        
        # Delete task command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', type=int, help='Task ID')
        
        args = parser.parse_args()
        
        if args.command == 'add':
            add_task(args.description)
        elif args.command == 'list':
            list_tasks()
        elif args.command == 'complete':
            complete_task(args.id)
        elif args.command == 'delete':
            delete_task(args.id)
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
