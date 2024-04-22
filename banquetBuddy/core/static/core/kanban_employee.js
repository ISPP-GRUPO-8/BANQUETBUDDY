document.addEventListener('DOMContentLoaded', function() {
    const tasks = document.querySelectorAll('.task[draggable="true"]');
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
        e.target.classList.add('dragging');
    }

    function handleDragEnd(e) {
        e.target.classList.remove('dragging');
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    function handleDrop(e) {
        e.preventDefault();
        const taskId = e.dataTransfer.getData('text');
        const newState = e.target.closest('.kanban-column').dataset.state;
        updateTaskState(taskId, newState);
    }

    function updateTaskState(taskId, newState) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch(`/employee/update_task_state/${taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ newState: newState })
        }).then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload(); // Actualizar la página para reflejar el cambio de estado
            } else {
                alert('Error updating task: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error updating task:', error);
        });
    }
});
