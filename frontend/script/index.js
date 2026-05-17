// Инициализация VK Bridge
vkBridge.send("VKWebAppInit", {})
  .then(data => {
    console.log("VK Bridge инициализирован!", data);
  })
  .catch(error => {
    console.error("Ошибка инициализации моста:", error);
  });

// Используем window, чтобы избежать ошибки "Identifier 'API_URL' has already been declared"
window.API_URL = 'https://todo-stasnau.amvera.io';

// Хелпер для безопасного чтения данных (учитывает пробелы в ключах бэкенда, если они есть)
function getField(obj, key) {
    return obj[key] || obj[key + ' '] || obj[' ' + key];
}

// Безопасно находим форму на странице
const devForm = document.getElementById('dev-form');

if (devForm) {
    devForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const vkIdInput = document.getElementById('dev-vk-id');
        const nameInput = document.getElementById('dev-name');
        const passwordInput = document.getElementById('dev-password');
        const errorDiv = document.getElementById('dev-error');
        const btn = document.getElementById('dev-login-btn');
        
        const vkId = vkIdInput.value.trim();
        const name = nameInput.value.trim();
        const password = passwordInput.value.trim();

        errorDiv.textContent = '';

        if (!vkId || !name) {
            errorDiv.textContent = 'Заполните VK ID и имя!';
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Проверка...';

        try {
            // Запрос проверки пароля с использованием глобального URL
            const passRes = await fetch(`${window.API_URL}/check-password`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "ngrok-skip-browser-warning": "true"
                },
                body: JSON.stringify({ password })
            });
            const passData = await passRes.json();
            
            if (!passData.valid) {
                errorDiv.textContent = 'Неправильный пароль';
                btn.disabled = false;
                btn.textContent = 'Зарегистрировать и войти';
                return;
            }
        } catch (e) {
            errorDiv.textContent = 'Нет связи с сервером!';
            console.error(e);
            btn.disabled = false;
            btn.textContent = 'Зарегистрировать и войти';
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Регистрация...';

        try {
            // Регистрация пользователя
            const res = await fetch(`${window.API_URL}/user/register?vk_id=${vkId}&name=${encodeURIComponent(name)}`, { 
                method: 'POST' 
            });
            const data = await res.json();

            // Читаем статус
            const status = getField(data, 'status')?.trim();
            
            if (status === 'already_exist' || status === 'user_created') {
                // Читаем данные
                const userId = getField(data, 'id');
                const userVk = getField(data, 'vk_id');
                const userName = getField(data, 'name');

                // Сохраняем в LocalStorage
                localStorage.setItem('user_id', userId);
                localStorage.setItem('vk_id', userVk);
                localStorage.setItem('user_name', userName);
                
                // Проверяем, есть ли уже семья
                try {
                    const famRes = await fetch(`${window.API_URL}/user/load_user_family?vk_id=${userVk}`);
                    const famData = await famRes.json();
                    const famStatus = getField(famData, 'status')?.trim();

                    if (famStatus === 'family_found') {
                        // Уже в семье -> сохраняем family_id и идём сразу в задачи
                        const familyId = getField(famData, 'family_id');
                        localStorage.setItem('family_id', familyId);
                        window.location.href = 'tasks.html';
                    } else {
                        // Семьи нет -> идём на choose.html
                        window.location.href = 'choose.html';
                    }
                } catch (famErr) {
                    // Если проверка семьи упала — всё равно идём на choose.html
                    console.warn('Не удалось проверить семью, переход на choose.html', famErr);
                    window.location.href = 'choose.html';
                }
                
            } else {
                errorDiv.textContent = 'Ошибка: ' + status;
            }
        } catch (e) {
            errorDiv.textContent = 'Нет связи с сервером!';
            console.error(e);
        } finally {
            btn.disabled = false;
            btn.textContent = 'Зарегистрировать и войти';
        }
    });
} else {
    console.log("Форма #dev-form не найдена на текущей странице, инициализация события пропущена.");
}
