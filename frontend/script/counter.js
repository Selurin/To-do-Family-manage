document.addEventListener('DOMContentLoaded', () => {
    const MAX_LENGTH = 255;
    const titleInput = document.getElementById('task-title');
    const charsLeftSpan = document.getElementById('chars-left');
    const counterDiv = document.getElementById('char-counter');
    const createBtn = document.getElementById('create-btn');

    // Защита от отсутствия элементов на странице
    if (!titleInput || !charsLeftSpan || !counterDiv || !createBtn) return;

    function updateCounter() {
        const currentLength = titleInput.value.length;
        const remaining = MAX_LENGTH - currentLength;

        charsLeftSpan.textContent = remaining;

        if (remaining < 0) {
            counterDiv.classList.add('warning');
            createBtn.disabled = true;
            createBtn.style.opacity = '0.5';
            createBtn.style.cursor = 'not-allowed';
        } 
        else {
            createBtn.disabled = false;
            createBtn.style.opacity = '1';
            createBtn.style.cursor = 'pointer';
        }
    }

    // Инициализация при загрузке
    updateCounter();
    // Отслеживание ввода
    titleInput.addEventListener('input', updateCounter);
});