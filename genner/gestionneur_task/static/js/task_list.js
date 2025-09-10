document.addEventListener('DOMContentLoaded', function () {
    function checkTasks() {
        const now = new Date();
        const nowDate = now.toISOString().split('T')[0];
        const nowTime = now.toTimeString().slice(0, 5);
        const rows = document.querySelectorAll('tbody tr[data-task-date]');
        const matchedTasks = [];

        rows.forEach(row => {
            if (row.dataset.taskDate === nowDate && row.dataset.taskHeure === nowTime) {
                matchedTasks.push(row.dataset.taskTitre);
            }
        });

        if (matchedTasks.length > 0) {
            const bodyText = matchedTasks.map(titre => `- ${titre}`).join('\n');

            if (Notification.permission === 'granted') {
                new Notification('Rappels de Tâches', {
                    body: `Tu dois commencer ces tâches à ${nowTime}:\n${bodyText}`,
                });
            } else {
                alert(`Tu dois commencer ces tâches à ${nowTime}:\n${bodyText}`);
            }
        }
    }

    const now = new Date();
    const delayToNextMinute = 60000 - (now.getSeconds() * 1000 + now.getMilliseconds());

    setTimeout(() => {
        checkTasks();
        setInterval(checkTasks, 60000);
    }, delayToNextMinute);

    if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
        Notification.requestPermission();
    }
});
