# Task Scheduler Project

## Overview

This project is a Task Scheduler application implemented in two different programming paradigms: functional programming and imperative programming. The goal of this project is to demonstrate the differences between these paradigms and to provide a practical example of how to implement the same functionality using both approaches.

## Functional Programming Implementation

The functional programming version of the Task Scheduler is implemented in `functional.py`. This version emphasizes immutability, no side effects, first-class functions, higher-order programming, and recursion.

### Key Concepts

1. **Immutability**: Variables and data structures are not modified after they are created. Instead, new versions are created with the necessary changes.
2. **No Side Effects**: Functions do not modify any state outside their scope. They return new values instead of modifying existing ones.
3. **First-Class Functions**: Functions are treated as first-class citizens, meaning they can be passed as arguments to other functions, returned as values, and assigned to variables.
4. **Higher-Order Programming**: Functions that take other functions as arguments or return them as results.
5. **Recursion**: Functions call themselves to perform repetitive tasks instead of using loops.

### Implementation Details

- **Task Creation**: Tasks are created using the `create_task` function.
- **Task Management**: Tasks are managed using recursive functions like `append`, `map`, `filter`, and `for_each`.
- **User Interaction**: User input is handled using the `get_input` function, which validates input using regular expressions.
- **Task Operations**: Tasks can be added, updated, deleted, filtered, sorted, and notified using various functions.
- **File Operations**: Tasks can be saved to and loaded from a file using `save_tasks` and `load_tasks`.

## Imperative Programming Implementation

The imperative programming version of the Task Scheduler is implemented in `imperative.py`. This version emphasizes mutable variables, side effects, loops, and straightforward procedural code.

### Key Concepts

1. **Mutable Variables**: Variables can be modified after they are created.
2. **Side Effects**: Functions can modify state outside their scope.
3. **Loops**: Repetitive tasks are performed using loops.
4. **Procedural Code**: Code is written in a straightforward, step-by-step manner.

### Implementation Details

- **Task Class**: Tasks are represented as instances of the `Task` class.
- **Task Scheduler Class**: The `TaskScheduler` class manages tasks using methods that modify the internal state.
- **User Interaction**: User input is handled using the `get_input` function, which validates input using regular expressions.
- **Task Operations**: Tasks can be added, updated, deleted, filtered, sorted, and notified using methods of the `TaskScheduler` class.
- **File Operations**: Tasks can be saved to and loaded from a file using `save_tasks` and `load_tasks`.

## Purpose

The purpose of this project is to provide a practical example of how to implement the same functionality using different programming paradigms. By comparing the functional and imperative implementations, we can better understand the strengths and weaknesses of each approach and learn how to think using different paradigms.

## How to Run

1. Ensure you have Python installed on your system.
2. Run the functional version:
   ```sh
   python functional.py
   ```
3. Run the imperative version:
   ```sh
   python imperative.py
   ```

## Conclusion

This project demonstrates how the same task scheduler functionality can be implemented using both functional and imperative programming paradigms. By studying these implementations, we can gain a deeper understanding of different programming paradigms and improve our ability to think and code in multiple ways.