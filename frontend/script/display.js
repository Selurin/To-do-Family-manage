// display.js - Отображение кода семьи, роли пользователя и имени семьи

console.log(" Файл display.js загружен");

const API_URL = 'https://todo-stasnau.amvera.io';


// Безопасное обновление текста элемента
function setTextContent(elementId, text, fallback = '', errorStyle = false) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = text || fallback;
        if (errorStyle && !text) {
            el.style.color = '#ff6b6b';
        }
    }
}

// ===== Загрузка имени семьи с бэкенда =====
async function loadFamilyName() {
    const inviteCode = localStorage.getItem('invite_code');
    if (!inviteCode) {
        console.warn(' invite_code не найден в localStorage');
        return;
    }

    try {
        const res = await fetch(`${API_URL}/family/get-by-code?invite_code=${encodeURIComponent(inviteCode)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const data = await res.json();
        
        if (data?.name) {
            const familyTitleDisplay = document.getElementById('family-title');
            if (familyTitleDisplay) {
                familyTitleDisplay.textContent = data.name.toUpperCase();
            }
            // Кэшируем имя, чтобы не запрашивать каждый раз
            localStorage.setItem('family_name', data.name);
            console.log(' Имя семьи загружено:', data.name);
        }
    } catch (e) {
        console.error(' Не удалось загрузить имя семьи:', e);
        const familyTitleDisplay = document.getElementById('family-title');
        if (familyTitleDisplay) {
            familyTitleDisplay.textContent = 'СЕМЬЯ';
        }
    }
}

// ===== Основная инициализация =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM загружен, инициализация display.js');

    // 1. Код приглашения (используется на created.html и settings.html)
    const inviteCode = localStorage.getItem('invite_code');
    console.log(' Код из localStorage:', inviteCode);

    setTextContent('invite-code', inviteCode, 'Не найден', true);
    setTextContent('family-code', inviteCode, 'Не найден', true);

    // 2. Роль пользователя (settings.html)
    const userRole = localStorage.getItem('user_role');
    setTextContent('user-role', userRole, 'Не определена');

    // 3. Имя семьи в заголовке (tasks.html)
    const familyTitleDisplay = document.getElementById('family-title');
    if (familyTitleDisplay) {
        const cachedName = localStorage.getItem('family_name');
        if (cachedName) {
            // Используем кэш — мгновенно
            familyTitleDisplay.textContent = cachedName.toUpperCase();
            console.log('Имя семьи взято из кэша:', cachedName);
        } else {
            // Кэша нет — запрашиваем с бэкенда
            console.log(' Кэш пуст, запрашиваем имя семьи с сервера...');
            loadFamilyName();
        }
    }
});

// // ===== Публичные функции для внешнего вызова =====

// // Обновить все отображаемые данные (например, после изменения настроек)
// function refreshDisplay() {
//     console.log(' refreshDisplay вызван');
//     // Можно точечно обновить элементы, но для надёжности — перезагрузка
//     location.reload();
// }

// // Принудительно перезагрузить имя семьи (например, после создания/входа в семью)
// async function refreshFamilyName() {
//     localStorage.removeItem('family_name'); // Сброс кэша
//     await loadFamilyName();
// }

// // Экспортируем функции для использования в других модулях (если нужно)
// window.displayUtils = {
//     refreshDisplay,
//     refreshFamilyName,
//     loadFamilyName
// };
