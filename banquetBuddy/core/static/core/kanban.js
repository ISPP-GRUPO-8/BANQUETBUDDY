document.addEventListener('DOMContentLoaded', function() {
    console.log("Kanban JS loaded and running");

    const board = document.querySelector('.kanban-board');
    board.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-edit')) {
            event.preventDefault();
            const taskId = event.target.closest('.task').dataset.taskId;
            loadTaskData(taskId);
        }
    });
    
    const tasks = document.querySelectorAll('.task');
    tasks.forEach(task => {
        task.addEventListener('dragstart', handleDragStart);
        task.addEventListener('dragend', handleDragEnd);
    });

    const columns = document.querySelectorAll('.kanban-column');
    columns.forEach(column => {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('drop', handleDrop);
    });

    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const taskId = this.closest('.task').dataset.taskId;
            loadTaskData(taskId);
        });
    });

    function loadTaskData(taskId) {
        fetch(`/get_task_data/?task_id=${taskId}`)
        .then(response => response.text())
        .then(html => {
            document.querySelector('#editTaskModal .modal-body').innerHTML = html;
            $('#editTaskModal').modal('show');
        })
        .catch(error => {
            console.error('Error loading task data:', error);
        });
    }

    // Función para enviar el formulario modificado
    document.querySelector('#editTaskModal .btn-primary').addEventListener('click', function() {
        document.querySelector('#editTaskModal form').submit();
    });
    

    function submitEditForm() {
        const form = document.querySelector('#editTaskModal form');
        const formData = new FormData(form);
        const taskId = form.querySelector('[name="task_id"]').value;
        fetch(`/update_task/${taskId}/`, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Task updated successfully:', data);
            $('#editTaskModal').modal('hide');
            // Actualizar la información de la tarea en la interfaz de usuario aquí, si es necesario
        }).catch(error => {
            console.error('Error updating task:', error);
        });
    }


    function handleDragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.dataset.taskId);
        e.target.style.opacity = '0.4';
        console.log("Dragging task:", e.target.dataset.taskId);
    }
    
    function handleDragEnd(e) {
        e.target.style.opacity = '';
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    function handleDrop(e) {
        e.preventDefault();
        const taskId = e.dataTransfer.getData('text');
        const newState = e.target.closest('.kanban-column').dataset.state;
        console.log(`Dropped task ${taskId} into new state ${newState}`);
        updateTaskState(taskId, newState);
    }
    
    function updateTaskState(taskId, newState) {
        const csrfToken = getCSRFToken();
        fetch(`/update_task_state/${taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ newState: newState })
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Task updated successfully:', data);
            refreshTaskInDOM(taskId, newState);
        }).catch(error => {
            console.log('Error updating task:', error);
        });
    }
    
    function refreshTaskInDOM(taskId, newState) {
        const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
        if (taskElement) {
            console.log("Task element found, removing from old parent.");
            const oldParent = taskElement.parentNode;
            oldParent.removeChild(taskElement);
            const targetColumn = document.querySelector(`.kanban-column.${newState.toLowerCase()} .tasks`);
            if (targetColumn) {
                console.log("Target column found, appending task.");
                targetColumn.appendChild(taskElement);
            } else {
                console.log("Failed to find the target column for state:", newState);
            }
        } else {
            console.log("Failed to find the task element for:", taskId);
        }
    }

    

    function getCSRFToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    }

    
});
