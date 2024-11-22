
# Task Scheduler / Planner Implementation in OZ

## Overview

This project involves implementing a **Task Scheduler/Planner** in OZ using two paradigms:
1. **Functional Paradigm**
2. **Imperative Paradigm**

# THIS SHOULD INCLUDE A DATABASE - NOT SHURE HOW THOUGH #

The goal is to explore how different programming paradigms impact the design and implementation of software.

---

## Functional Paradigm Implementation

### Data Representation
- Tasks are represented as **records**.
  ```oz
  Task = task(id: ID description: Description dueDate: DueDate priority: Priority status: Status)
  ```
- Tasks are stored in **immutable lists**.

### Core Operations
1. **Add Task**: Create a function that returns a new list with the new task appended.
   ```oz
   fun {AddTask TaskList NewTask}
      NewTaskList = TaskList | NewTask
   end
   ```

2. **Update Task**: Traverse the list recursively to modify a specific task based on its ID.
   ```oz
   fun {UpdateTask TaskList ID UpdatedTask}
      case TaskList of
         nil then nil
      [] T|Ts then
         if T.id == ID then UpdatedTask|Ts
         else T|{UpdateTask Ts ID UpdatedTask}
         end
      end
   end
   ```

3. **Delete Task**: Filter out the task with the given ID.
   ```oz
   fun {DeleteTask TaskList ID}
      {Filter TaskList fun {$ T} T.id \= ID end}
   end
   ```

4. **Filter and Sort Tasks**: Use higher-order functions like `Map` and `Fold` for filtering and sorting.

### Persistence
- Write tasks to a file:
  ```oz
  proc {SaveTasks TaskList FileName}
     File = {New Open.file write FileName}
     {ForEach TaskList fun {$ Task} 
        {File.write Task#
          ""}
     end}
  end
  ```

- Read tasks from a file and convert them into records.

### Notifications
- Highlight tasks nearing deadlines or overdue using declarative logic.

---

## Imperative Paradigm Implementation

### Data Representation
- Use a **mutable cell** to store tasks dynamically.
  ```oz
  {NewCell [] Tasks}
  ```

### Core Operations
1. **Add Task**: Append tasks to the mutable cell.
   ```oz
   proc {AddTask Tasks NewTask}
      Tasks := NewTask|@Tasks
   end
   ```

2. **Update Task**: Iterate over the mutable list to update the target task.
   ```oz
   proc {UpdateTask Tasks ID UpdatedTask}
      Tasks := {Map @Tasks fun {$ T}
         if T.id == ID then UpdatedTask else T end
      end}
   end
   ```

3. **Delete Task**: Remove the task with the given ID directly.
   ```oz
   proc {DeleteTask Tasks ID}
      Tasks := {Filter @Tasks fun {$ T} T.id \= ID end}
   end
   ```

4. **Filter and Sort Tasks**: Use loops or built-in sorting constructs.

### Persistence
- Use file handling to read/write tasks using procedural constructs.

### Notifications
- Use loops and conditions to evaluate and notify users about deadlines.

---

## Work Plan - not strict

### Week 1: Preparation
1. Set up the OZ development environment.
2. Define task data structures using records.
3. Prototype the task scheduler.

### Week 2: Functional Paradigm
1. Implement:
   - Add, update, and delete tasks.
   - Filter and sort tasks.
2. Add notifications and file I/O declaratively.
3. Test all functionalities.

### Week 3: Imperative Paradigm
1. Implement:
   - Add, update, and delete tasks.
   - Filter and sort tasks.
2. Integrate notifications and file I/O imperatively.
3. Test all functionalities.

### Week 4: Comparison and Refinement
1. Compare functional and imperative implementations in OZ.
2. Optimize code for performance and usability.
3. Document the strengths and weaknesses of both paradigms.

---
