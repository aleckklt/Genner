document.addEventListener('DOMContentLoaded', function () {
    setInterval(() => {
        const now = new Date();
        const nowDate = now.toISOString().split('T')[0];
        const nowTime = now.toTimeString().slice(0, 5);
        const rows = document.querySelectorAll('tbody tr[data-task-date]');
        rows.forEach(row => {
            if (row.dataset.taskDate === nowDate && row.dataset.taskHeure === nowTime) {
                const titre = row.dataset.taskTitre;
                if (Notification.permission === 'granted') {
                    new Notification('Rappel de Tâche', {
                        body: `Tu dois commencer cette tâche : ${titre} à ${nowTime}`,
                    });
                } else {
                    alert(`Tu dois commencer cette tâche : ${titre} à ${nowTime}`);
                }
            }
        });
    }, 60000);
});
