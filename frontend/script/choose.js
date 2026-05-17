const API_URL = 'https://todo-stasnau.amvera.io';
        const statusMsg = document.getElementById('status-msg');
        const btnCreate = document.getElementById('btn-create');
        const btnJoin = document.getElementById('btn-join');

        // Регистрация / получение ID пользователя
        async function ensureUserRegistered(vk_id, name) {
            try {
                const res = await fetch(`${API_URL}/user/register?vk_id=${vk_id}&name=${encodeURIComponent(name)}`, { 
                    method: 'POST' 
                });
                const data = await res.json();
                
                if (data.status === 'already_exist' || data.status === 'user_created') {
                    // Сохраняем в localStorage, чтобы не ходить на бэк каждый раз
                    localStorage.setItem('user_id', data.id);
                    localStorage.setItem('vk_id', data.vk_id);
                    localStorage.setItem('user_name', data.name);
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

        //  Проверка: состоит ли пользователь уже в семье
        async function checkFamilyStatus(vk_id) {
            try {
                const res = await fetch(`${API_URL}/user/load_user_family?vk_id=${vk_id}`);
                const data = await res.json();
                
                if (data.status === 'family_found') {
                    localStorage.setItem('family_id', data.family_id);
                    statusMsg.textContent = '✅ Семья найдена, переходим...';
                    // Перенаправляем на страницу задач
                    setTimeout(() => window.location.href = 'tasks.html', 500);
                    return true;
                }
                return false;
            } catch (e) {
                console.error(e);
                return false;
            }
        }

        //  Инициализация при загрузке страницы
        document.addEventListener('DOMContentLoaded', async () => {
            // Для разработки берём данные из localStorage. 
            // В продакшене здесь будет вызов VK Bridge для получения vk_id и имени
            let vk_id = localStorage.getItem('vk_id');
            let name = localStorage.getItem('user_name');

            if (!vk_id || !name) {
                statusMsg.textContent = '⚠️ Сначала авторизуйтесь на главной странице';
                setTimeout(() => window.location.href = 'index.html', 2000);
                return;
            }

            statusMsg.textContent = '⏳ Загрузка...';

            // Гарантируем, что пользователь есть в БД
            const user_id = await ensureUserRegistered(vk_id, name);
            if (!user_id) return;

            // Проверяем, есть ли уже семья
            const hasFamily = await checkFamilyStatus(vk_id);
            if (hasFamily) return; // Уже перенаправили на tasks.html

            // Если семьи нет, разблокируем кнопки выбора
            statusMsg.textContent = '';
            btnCreate.disabled = false;
            btnJoin.disabled = false;

            // Обработчики кнопок (просто переход на формы ввода)
            btnCreate.addEventListener('click', () => {
                window.location.href = 'create.html';
            });

            btnJoin.addEventListener('click', () => {
                window.location.href = 'join.html';
            });
        });
