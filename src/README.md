# CLI Task Manager

A command-line task management application that provides basic task tracking functionality through a terminal interface.

## What this code does

This application implements a simple task management system with four core operations:

- **Add tasks**: Create new tasks with text descriptions
- **List tasks**: Display all tasks with completion status indicators
- **Complete tasks**: Mark existing tasks as completed
- **Delete tasks**: Remove tasks from the system

Tasks are persisted in a local JSON file (`tasks.json`) that stores task objects with unique IDs, descriptions, and completion status. The application uses Python's built-in `argparse` module for command-line interface handling and includes input validation and error handling.

## Language and its use case

**Python 3** was selected for this implementation because:

- **Standard library**: Rich built-in modules (`argparse`, `json`, `os`) eliminate external dependencies
- **Readability**: Clear syntax makes the codebase maintainable and approachable
- **Cross-platform**: Works consistently across Windows, macOS, and Linux systems
- **Type hints**: Built-in support for annotations improves code clarity

Python excels at CLI tools, scripting, and rapid application development. However, for systems requiring microsecond-level latency or memory-constrained environments, languages like C++ or Rust would be more appropriate.

## Why this structure

**Single-file design** was chosen because:
- The application scope is small enough to maintain clarity in one file
- Reduces import complexity and potential circular dependencies
- Makes the codebase immediately understandable for evaluation
- Eliminates file navigation overhead

**src/ and docs/ separation** provides:
- Clear distinction between implementation and documentation
- Standard project organization that scales well
- Easy navigation for evaluators

**JSON persistence** was selected over alternatives because:
- Human-readable format allows easy inspection and debugging
- Native Python support without external dependencies
- Sufficient for the expected data volume (<1000 tasks)

## Key decisions

### 1. JSON storage vs database

**Chosen**: JSON file storage using Python's `json` module.

**Why**: JSON provides the right balance of readability and structure for this use case. It requires no external dependencies and allows manual data inspection during development and debugging.

**Alternative considered**: SQLite would offer ACID compliance and better query performance, but would add unnecessary complexity for a single-user CLI tool with simple data access patterns.

### 2. argparse vs manual parsing

**Chosen**: Python's built-in `argparse` module for CLI interface.

**Why**: `argparse` provides professional-grade CLI features including automatic help text generation, argument validation, and consistent error handling without additional code.

**Alternative considered**: Manual string parsing would reduce dependency overhead but would require significant boilerplate code for help generation, validation, and error handling.

## Known limitations

- **Concurrency control**: No file locking mechanism; simultaneous writes could corrupt data
- **Performance**: Linear search operations (O(n)) become inefficient with large datasets
- **Multi-user support**: No user isolation or authentication mechanisms
- **File-based storage**: Becomes a bottleneck under high I/O load
- **Task editing**: No ability to modify task descriptions after creation
- **Search functionality**: No filtering or search capabilities
- **Undo operations**: No way to recover from accidental deletions

## How to run the code

1. Navigate to the `src/` directory:
   ```bash
   cd src/
   ```

2. Run the application with Python 3:
   ```bash
   python3 main.py --help
   ```

3. Example usage:
   ```bash
   # Add a task
   python3 main.py add "Buy groceries"
   
   # List all tasks
   python3 main.py list
   
   # Mark task as completed
   python3 main.py complete 1
   
   # Delete a task
   python3 main.py delete 1
   ```

## If this scales

**Users increase**: The single-user design breaks immediately. No authentication, user isolation, or concurrent access control exists.

**Data increases**: With thousands of tasks, linear search operations become slow. File I/O operations take longer, and memory usage grows linearly with task count.

**Requests increase**: The file-based approach cannot handle concurrent operations. Race conditions during file operations would lead to data corruption without proper locking mechanisms.

## What I would improve next

1. **File locking**: Implement proper file locking to prevent race conditions
2. **Task editing**: Add ability to modify existing task descriptions
3. **Search and filter**: Implement text search and status filtering
4. **Configuration**: Make the tasks file path configurable via environment variables
5. **Unit tests**: Add comprehensive test coverage for all functions
6. **Logging**: Replace print statements with structured logging
7. **Task priorities**: Add priority levels with sorting capabilities
