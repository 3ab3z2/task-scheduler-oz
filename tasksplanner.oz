functor
import 
    System
    OS
    File
    TextIO
    Tk
export
    runTUI: RunTUI
define
    % Task record definition
    TaskRecord = {NewName}

    % Ensure tasks folder exists
    fun {EnsureTasksFolder}
        OsName = {OS.name}
        FolderPath = case OsName 
                     of 'windows' then "tasks\\"
                     else "tasks/" 
                     end
    in
        try 
            if {Not {File.exists FolderPath}} then
                {OS.mkdir FolderPath}
            end
            FolderPath
        catch _ then 
            {System.show 'Could not create tasks folder'}
            "."
        end
    end

    % Save task to file
    proc {SaveTaskToFile Task}
        FolderPath = {EnsureTasksFolder}
        FileName = FolderPath#{VirtualString.toString Task.id}#".txt"
        File
    in
        File = {TextIO.openFile FileName [write]}
        {TextIO.writeFile File {VirtualString.toString Task.title}#"\n"}
        {TextIO.writeFile File {VirtualString.toString Task.description}#"\n"}
        {TextIO.writeFile File {VirtualString.toString Task.deadline}#"\n"}
        {TextIO.writeFile File {VirtualString.toString Task.completed}#"\n"}
        {TextIO.closeFile File}
    end

    % Load tasks from files
    fun {LoadTasks}
        FolderPath = {EnsureTasksFolder}
        Files = {OS.listDir FolderPath}
    in
        {List.map 
            {List.filter Files fun {$ F} {String.isSubstring F ".txt"} end}
            fun {$ FileName}
                FilePath = FolderPath#FileName
                File = {TextIO.openFile FilePath [read]}
                Title = {TextIO.readLine File}
                Description = {TextIO.readLine File}
                Deadline = {TextIO.readLine File}
                Completed = {TextIO.readLine File}
                ID = {String.toInt {String.substring FileName 0 {String.length FileName}-4}}
            in
                {TextIO.closeFile File}
                {CreateTask ID 
                    {String.trim Title} 
                    {String.trim Description} 
                    {String.trim Deadline} 
                    {String.trim Completed} == "true"}
            end}
    end

    % Functional Implementation
    fun {CreateTask ID Title Description Deadline Completed}
        {Record.make TaskRecord 
         [id#ID title#Title description#Description deadline#Deadline completed#Completed]}
    end

    fun {AddTask Tasks NewTask}
        NewTask|Tasks
    end

    fun {RemoveTask Tasks ID}
        {List.filter Tasks fun {$ Task} Task.id \= ID end}
    end

    fun {MarkTaskComplete Tasks ID}
        {List.map Tasks fun {$ Task}
            if Task.id == ID then
                {Record.adjoin Task completed#true}
            else Task end
        end}
    end

    fun {EditTask Tasks ID NewTitle NewDescription NewDeadline}
        {List.map Tasks fun {$ Task}
            if Task.id == ID then
                {Record.adjoin Task 
                 [title#NewTitle 
                  description#NewDescription 
                  deadline#NewDeadline]}
            else Task end
        end}
    end

    % Task Manager Class
    class TaskManager
        attr tasks
        meth init
            tasks := {LoadTasks}
        end
        
        meth addTask(Title Description Deadline)
            ID = case @tasks 
                 of nil then 1 
                 else {Length @tasks} + 1 
                 end
            NewTask = {CreateTask ID Title Description Deadline false}
        in
            tasks := {AddTask @tasks NewTask}
            {SaveTaskToFile NewTask}
        end
        
        meth removeTask(ID)
            tasks := {RemoveTask @tasks ID}
            FolderPath = {EnsureTasksFolder}
            FileName = FolderPath#{VirtualString.toString ID}#".txt"
        in
            if {File.exists FileName} then
                {File.remove FileName}
            end
        end
        
        meth markComplete(ID)
            Tasks = {MarkTaskComplete @tasks ID}
            Task = {List.find Tasks fun {$ T} T.id == ID end}
        in
            tasks := Tasks
            {SaveTaskToFile Task}
        end
        
        meth editTask(ID NewTitle NewDescription NewDeadline)
            Tasks = {EditTask @tasks ID NewTitle NewDescription NewDeadline}
            Task = {List.find Tasks fun {$ T} T.id == ID end}
        in
            tasks := Tasks
            {SaveTaskToFile Task}
        end
        
        meth getTasks(Tasks)
            Tasks = @tasks
        end
    end

    % UI Procedures
    proc {AddTaskUI Manager}
        Title = {Tk.getString "Enter task title:"}
        Description = {Tk.getString "Enter task description:"}
        Deadline = {Tk.getString "Enter task deadline:"}
    in
        {Manager addTask(Title Description Deadline)}
        {Tk.showInfo "Task added successfully!"}
    end

    proc {RemoveTaskUI Manager}
        ID = {Tk.getInt "Enter task ID to remove:"}
    in
        {Manager removeTask(ID)}
        {Tk.showInfo "Task removed successfully!"}
    end

    proc {MarkCompleteUI Manager}
        ID = {Tk.getInt "Enter task ID to mark complete:"}
    in
        {Manager markComplete(ID)}
        {Tk.showInfo "Task marked as complete!"}
    end

    proc {EditTaskUI Manager}
        ID = {Tk.getInt "Enter task ID to edit:"}
        NewTitle = {Tk.getString "Enter new task title:"}
        NewDescription = {Tk.getString "Enter task description:"}
        NewDeadline = {Tk.getString "Enter task deadline:"}
    in
        {Manager editTask(ID NewTitle NewDescription NewDeadline)}
        {Tk.showInfo "Task edited successfully!"}
    end

    proc {ViewTasksUI Manager}
        Tasks
    in
        {Manager getTasks(Tasks)}
        {Tk.showInfo {List.foldL Tasks 
            fun {$ Acc Task}
                Acc#{VirtualString.toString Task.id}#": "#{VirtualString.toString Task.title}#" (Completed: "#{VirtualString.toString Task.completed}#")\n"
            end ""}}
    end

    proc {RunTUI}
        Manager = {New TaskManager init}
    in
        {Tk.init}
        {Tk.createMenu 
            [menuItem("Add Task"     proc {$} {AddTaskUI Manager} end)
             menuItem("Remove Task"  proc {$} {RemoveTaskUI Manager} end)
             menuItem("Mark Complete" proc {$} {MarkCompleteUI Manager} end)
             menuItem("Edit Task"    proc {$} {EditTaskUI Manager} end)
             menuItem("View Tasks"   proc {$} {ViewTasksUI Manager} end)]}
        {Tk.startEventLoop}
    end

    % Start the application
    {RunTUI}
end