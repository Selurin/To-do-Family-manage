// profile.js - Загрузка и отображение участников семьи

console.log("Файл profile.js загружен!");

// Определяем API_URL для profile.js
const API_URL = window.API_URL || 'https://todo-stasnau.amvera.io';


// Перевод роли на русский + иконка
function getRoleBadge(role) {
    const roles = {
        'owner': { label: 'Создатель', icon: '👑', color: '#ffd700' },
        'parent': { label: 'Родитель', icon: '🧑', color: '#4ecdc4' },
        'child': { label: 'Ребёнок', icon: '🧒', color: '#95e1d3' }
    };
    return roles[role] || { label: role, icon: '👤', color: '#ccc' };
}

// ===== Загрузка участников семьи =====
async function loadFamilyMembers() {
    const membersList = document.getElementById('members-list');
    if (!membersList) return;

    // Получаем family_id: сначала из кэша, иначе через invite_code
    let familyId = localStorage.getItem('family_id');
    
    if (!familyId) {
        const inviteCode = localStorage.getItem('invite_code');
        if (!inviteCode) {
            membersList.innerHTML = '<li class="error">Код семьи не найден</li>';
            return;
        }
        // Запрашиваем данные семьи, чтобы получить family_id
        try {
            const res = await fetch(`${API_URL}/family/get-by-code?invite_code=${encodeURIComponent(inviteCode)}`);
            if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
            const familyData = await res.json();
            familyId = familyData.id;
            // Кэшируем для будущих запросов
            localStorage.setItem('family_id', familyId);
        } catch (e) {
            console.error('Не удалось получить family_id:', e);
            membersList.innerHTML = '<li class="error">Ошибка загрузки семьи: ' + escapeHtml(e.message) + '</li>';
            return;
        }
    }

    // Загружаем участников по family_id
    try {
        membersList.innerHTML = '<li class="loading">Загрузка...</li>';
        
        const res = await fetch(`${API_URL}/members/family/${familyId}`);
        if (!res.ok) {
            let errorMsg = `HTTP ${res.status}`;
            try {
                const errData = await res.json();
                errorMsg = errData.detail || errorMsg;
            } catch (parseErr) { /* игнорируем если ответ не JSON */ }
            throw new Error(errorMsg);
        }
        
        const members = await res.json();
        
        if (!Array.isArray(members)) {
            membersList.innerHTML = '<li class="error">Неверный формат данных от сервера</li>';
            return;
        }

        if (members.length === 0) {
            membersList.innerHTML = '<li class="empty"> В семье пока нет участников</li>';
            return;
        }

        // Рендерим список
        membersList.innerHTML = '';
        const currentUserId = localStorage.getItem('user_id');
        
        members.forEach(member => {
            const li = document.createElement('li');
            li.className = 'member-item';
            if (member.user_id == currentUserId) {
                li.classList.add('current-user');
            }
            
            const roleInfo = getRoleBadge(member.role);
            const isMe = member.user_id == currentUserId ? ' (вы)' : '';
            
            li.innerHTML = `
                
                <div class="member-info">
                    <div class="member-name">
                        ${member.nickname || member.name || 'Аноним'}${isMe}
                    </div>
                    <div class="member-role" style="color: ${roleInfo.color}">
                        ${roleInfo.icon} ${roleInfo.label}
                    </div>
                </div>
            `;
            membersList.appendChild(li);
        });
        
        console.log(`Загружено ${members.length} участников`);
        
      } catch (e) {
            console.error('Ошибка загрузки участников:', e);
            const errorText = e instanceof Error ? e.message : 'Неизвестная ошибка';
            membersList.innerHTML = '<li class="error">Ошибка: ' + escapeHtml(errorText) + '</li>';
        }
}

// ===== Инициализация =====
document.addEventListener('DOMContentLoaded', () => {
    // Отображение имени текущего пользователя
    const profileUserName = document.getElementById('profile-user-name');
    if (profileUserName) {
        const userName = localStorage.getItem('user_name') || 'Пользователь';
        profileUserName.textContent = 'Вы: ' + userName;
    }
    
    // Загрузка списка участников
    loadFamilyMembers();
});

// ===== Утилиты =====

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== Публичные функции =====
window.membersUtils = {
    loadFamilyMembers,
    getRoleBadge
};
