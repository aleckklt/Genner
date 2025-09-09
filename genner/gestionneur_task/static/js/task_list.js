document.addEventListener('DOMContentLoaded', function () {
    function checkTasks() {
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
    }

    const now = new Date();
    const delayToNextMinute = 60000 - (now.getSeconds() * 1000 + now.getMilliseconds());

    setTimeout(() => {
        checkTasks();
        setInterval(checkTasks, 60000);
    }, delayToNextMinute);
});