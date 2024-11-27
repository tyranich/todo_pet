// Функция для получения списка задач
async function getDoList() {
    const response = await fetch('http://127.0.0.1:8000/read');
    
    console.log(response.url)

    const tasks = await response.json();

    const todoList = document.getElementById("todo-list");
    if (todoList) {
        clearElement(todoList); // Очищаем список перед добавлением
        
    }
    tasks.forEach(task => addTaskToDOM(task));
    
}

// Функция для добавления задачи в DOM
function addTaskToDOM(task) {
    const todoList = document.getElementById("todo-list");
    if (!todoList) return;

    const li = document.createElement("li");
    const dateComplete = formatDate(task.fields.date_complete);

    li.className = "list-group-item d-flex justify-content-between align-items-center";
    li.innerHTML = `
        <span class="task-text">${task.fields.task}</span>
        <span class="task-date">${dateComplete}</span>
        <div class="row row-edit" style="display: none;">
            ${generateEditFields(task.fields.task)}
        </div>
        <div class="btn-group">
            <button class="btn btn-danger btn-sm delete-btn" value="${task.pk}">&#x2715;</button>
            <button class="btn btn-primary btn-sm edit-btn" value="${task.pk}">&#9998;</button>
        </div>
    `;
    todoList.appendChild(li);
}

// Форматирование даты
function formatDate(date) {
    if (!date) return "";
    return new Date(date).toLocaleString("ru");
}

// Генерация HTML для полей редактирования
function generateEditFields(taskText) {
    return `
        <div class="col-6 ed1">
            <label for="end-time">Время завершения:</label>
            <input type="datetime-local" class="form-control end-time-edit">
        </div>
        <div class="col-6 ed2">
            <label for="reminder-time">Время напоминания:</label>
            <input type="datetime-local" class="form-control reminder-time-edit">
        </div>
        <div class="col-6 ed3">
            <label for="edit-input">Новый текст:</label>
            <input type="text" class="form-control edit-input" value="${taskText}">
        </div>
    `;
}

// Очищение содержимого элемента
function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

// Добавление новой задачи
async function addTask(formVal) {
    const csrftoken = getCookie('csrftoken');
    await fetch('http://127.0.0.1:8000/create', {
        method: 'POST',
        body: JSON.stringify(formVal),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    });
    getDoList(); // Обновляем список
}

// Удаление задачи
async function deleteTask(taskId) {
    const csrftoken = getCookie('csrftoken');
    await fetch('http://127.0.0.1:8000/delete', {
        method: 'POST',
        body: JSON.stringify({ task_id: taskId }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    });
}

// Редактирование задачи
async function editTask(data) {
    const csrftoken = getCookie('csrftoken');
    await fetch('http://127.0.0.1:8000/update', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    });
    getDoList(); // Обновляем список
}

// Инициализация событий
function initializeEventListeners() {
    const todoForm = document.getElementById("todo-form");
    if (todoForm) {
        getDoList()
        todoForm.addEventListener("submit", handleFormSubmit);

        document.getElementById("todo-list").addEventListener("click", handleListClick);
    }
}

// Обработка отправки формы
function handleFormSubmit(event) {
    event.preventDefault();

    const taskInput = document.getElementById("todo-input");
    const endTimeInput = document.getElementById("end-time");
    const remindTimeInput = document.getElementById("reminder-time");

    const formVal = {
        text_task: taskInput.value.trim(),
        end_time: endTimeInput.value,
        rem_time: remindTimeInput.value
    };

    if (formVal.text_task) {
        addTask(formVal);
        taskInput.value = "";
        endTimeInput.value = null;
        remindTimeInput.value = null;
    }
}

// Обработка кликов по списку задач
function handleListClick(event) {
    const target = event.target;

    if (target.classList.contains("delete-btn")) {
        target.parentElement.parentElement.remove();
        deleteTask(target.value);
    } else if (target.classList.contains("edit-btn")) {
        toggleEditMode(target);
    }
}

// Переключение режима редактирования
function toggleEditMode(button) {
    const taskText = button.parentElement.parentElement.querySelector(".task-text");
    const taskRowDate = button.parentElement.parentElement.querySelector(".row-edit");

    if (taskText.style.display !== "none") {
        taskText.style.display = "none";
        taskRowDate.style.display = "inline";
        button.innerHTML = "&#10004;";
    } else {
        const editTaskVal = {
            pk: button.value,
            newText: taskRowDate.querySelector(".edit-input").value,
            newDateEnd: taskRowDate.querySelector(".end-time-edit").value,
            newDateRem: taskRowDate.querySelector(".reminder-time-edit").value,
        };
        taskText.textContent = editTaskVal.newText;
        taskRowDate.style.display = "none";
        taskText.style.display = "inline";
        button.innerHTML = "&#9998;";
        editTask(editTaskVal);
    }
}

// Получение CSRF токена
function getCookie(name) {
    const cookies = document.cookie.split(';').map(cookie => cookie.trim());
    for (let cookie of cookies) {
        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(cookie.split('=')[1]);
        }
    }
    return null;
}

// Инициализация
initializeEventListeners();