const API_URL = 'https://todo-stasnau.amvera.io';

document.addEventListener('DOMContentLoaded', () => {
    // 🔴 КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: берем vk_id вместо user_id
    const vkId = localStorage.getItem('vk_id');
    
    if (!vkId) {
        window.location.href = 'index.html';
        return;
    }

    document.getElementById('create-family-btn').addEventListener('click', async () => {
        const nameInput = document.getElementById('family-name-input');
        const errorDiv = document.getElementById('create-error');
        const name = nameInput.value.trim();

        errorDiv.textContent = '';

        if (!name) {
            errorDiv.textContent = 'Введите имя семьи!';
            return;
        }

        try {
            // Передаем именно vk_id (как и ждет бэкенд)
            const res = await fetch(`${API_URL}/family/create?name=${encodeURIComponent(name)}&user_id=${vkId}`, {
                method: 'POST'
            });
            const data = await res.json();

            if (data.status === 'family created') {
                localStorage.setItem('family_id', data.family_id);
                localStorage.setItem('invite_code', data.invite_code);
                localStorage.setItem('family_name', data.name);
                
                // Передаем код в ссылку для экрана created.html (как делали на прошлом шаге)
                window.location.href = `created.html?invite_code=${data.invite_code}`;
            } else {
                errorDiv.textContent = 'Ошибка: ' + (data.error || 'Попробуйте позже');
            }
        } catch (e) {
            errorDiv.textContent = 'Нет связи с сервером';
            console.error(e);
        }
    });
});
