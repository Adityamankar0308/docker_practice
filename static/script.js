
const taskList = document.getElementById("taskList");
const taskInput = document.getElementById("taskInput");
const addTaskBtn = document.getElementById("addTaskBtn");


// Display all tasks
async function loadTasks() {

    try {
        const response = await fetch("/api/tasks");

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        const tasks = await response.json();

        taskList.innerHTML = "";

        tasks.forEach(task => {

            const li = document.createElement("li");

            const title = document.createElement("span");

            title.textContent = task.title;

            if (task.completed) {
                title.classList.add("completed");
            }


            // Complete or Undo button
            const completeBtn = document.createElement("button");

            completeBtn.textContent = task.completed
                ? "Undo"
                : "Complete";

            completeBtn.className = "complete-btn";

            completeBtn.addEventListener("click", () => {
                updateTask(task.id, !Boolean(task.completed));
            });


            // Delete button
            const deleteBtn = document.createElement("button");

            deleteBtn.textContent = "Delete";

            deleteBtn.className = "delete-btn";

            deleteBtn.addEventListener("click", () => {
                deleteTask(task.id);
            });


            // Button container
            const actions = document.createElement("div");

            actions.className = "actions";

            actions.appendChild(completeBtn);
            actions.appendChild(deleteBtn);


            li.appendChild(title);
            li.appendChild(actions);

            taskList.appendChild(li);

        });

    } catch (error) {

        console.error(error);

        taskList.textContent = "Could not load tasks.";

    }
}


// Add a new task
async function addTask() {

    const title = taskInput.value.trim();

    if (!title) {
        alert("Please enter a task!");
        return;
    }

    try {

        const response = await fetch("/api/tasks", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({ title })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not add task");
        }

        taskInput.value = "";

        await loadTasks();

    } catch (error) {

        alert(error.message);

    }
}


// Update task completion
async function updateTask(id, completed) {

    try {

        const response = await fetch(`/api/tasks/${id}`, {

            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({ completed })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not update task");
        }

        await loadTasks();

    } catch (error) {

        alert(error.message);

    }
}


// Delete task
async function deleteTask(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this task?"
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const response = await fetch(`/api/tasks/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not delete task");
        }

        await loadTasks();

    } catch (error) {

        alert(error.message);

    }
}


// Connect Add Task button
addTaskBtn.addEventListener("click", addTask);


// Load tasks when page opens
loadTasks();
