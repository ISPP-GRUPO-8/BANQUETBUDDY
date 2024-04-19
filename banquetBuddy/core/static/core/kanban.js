document.addEventListener('DOMContentLoaded', function() {
    console.log("Kanban JS is loaded and running");

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
