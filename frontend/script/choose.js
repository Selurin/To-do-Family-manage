const API_URL = 'https://todo-stasnau.amvera.io';
const statusMsg = document.getElementById('status-msg');
const btnCreate = document.getElementById('btn-create');
const btnJoin = document.getElementById('btn-join');

async function ensureUserRegistered(vk_id, name) {
    try {
        const res = await fetch(`${API_URL}/user/register?vk_id=${vk_id}&name=${encodeURIComponent(name)}`, { 
            method: 'POST' 
        });
        const data = await res.json();
        
        if (data.status === 'already_exist' || data.status === 'user_created') {
            try {
                localStorage.setItem('user_id', data.id);
                localStorage.setItem('vk_id', data.vk_id);
                localStorage.setItem('user_name', data.name);
            } catch (e) { /* Игнорируем блокировку localStorage */ }
            return data.id;
        } else {
            throw new Error(data.status || 'Ошибка регистрации');
        }
    } catch (e) {
        console.error(e);
        statusMsg.textContent = '❌ Нет связи с сервером';
        return null;
    }
}

async function checkFamilyStatus(vk_id) {
    try {
        const res = await fetch(`${API_URL}/user/load_user_family?vk_id=${vk_id}`);
        const data = await res.json();
        
        if (data.status === 'family_found') {
            try { localStorage.setItem('family_id', data.family_id); } catch(e){}
            statusMsg.textContent = '✅ Семья найдена, переходим...';
            setTimeout(() => window.location.href = 'tasks.html' + window.location.search, 500);
            return true;
        }
        return false;
    } catch (e) {
        console.error(e);
        return false;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    // 1. БЕРЕМ ID ИЗ ССЫЛКИ, КОТОРУЮ ПРОБРОСИЛ INDEX.JS
    const urlParams = new URLSearchParams(window.location.search);
    let vk_id = urlParams.get('vk_user_id') || localStorage.getItem('vk_id');
    let name = localStorage.getItem('user_name') || `Пользователь ${vk_id}`;

    // Если видим эту новую ошибку — значит, код обновился!
    if (!vk_id || vk_id === 'null') {
        statusMsg.textContent = '⚠️ Ошибка передачи данных от ВК. Возвращаем...';
        setTimeout(() => window.location.href = 'index.html' + window.location.search, 2500);
        return;
    }

    statusMsg.textContent = '⏳ Загрузка...';

    const user_id = await ensureUserRegistered(vk_id, name);
    if (!user_id) return;

    const hasFamily = await checkFamilyStatus(vk_id);
    if (hasFamily) return;

    statusMsg.textContent = '';
    btnCreate.disabled = false;
    btnJoin.disabled = false;

    btnCreate.addEventListener('click', () => {
        window.location.href = 'create.html' + window.location.search;
    });

    btnJoin.addEventListener('click', () => {
        window.location.href = 'join.html' + window.location.search;
    });
});
