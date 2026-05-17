const API_URL = 'https://todo-stasnau.amvera.io';

        document.addEventListener('DOMContentLoaded', async () => {
            const userId = localStorage.getItem('user_id');
            const vkId = localStorage.getItem('vk_id');

            // Защита от входа без авторизации
            // if (!userId || !vkId) {
            //     window.location.href = 'index.html';
            //     return;
            // }

            // Загружаем список членов семьи
            await loadFamilyMembers();

            document.getElementById('create-btn').addEventListener('click', async () => {
                const title = document.getElementById('task-title').value.trim();
                const desc = '';
                let toId = document.getElementById('executor-select').value;

                if (!title) {
                    alert('Введите название задачи');
                    return;
                }

                // Если выбрано "Я", подставляем ID пользователя
                if (toId === 'me') {
                    toId = userId;
                } else {
                    toId = parseInt(toId);
                }

                try {
                    const res = await fetch(
                        `${API_URL}/task/add_task?from_id=${userId}&to_id=${toId}&title=${encodeURIComponent(title)}&description=${encodeURIComponent(desc)}`,
                        { method: 'POST' }
                    );
                    const data = await res.json();

                    if (data.status?.trim() === 'task_assigned' || data.status?.trim() === 'task assigned') {
                        window.location.href = 'tasks.html';
                    } else {
                        alert('Ошибка: ' + (data.status || 'Попробуйте позже'));
                    }
                } catch (e) {
                    alert('Нет связи с сервером');
                    console.error(e);
                }
            });
        });

        // Загрузка членов семьи для выпадающего списка
        async function loadFamilyMembers() {
            const vkId = localStorage.getItem('vk_id');
            const currentUserId = localStorage.getItem('user_id');
            
            try {
                // Сначала получаем family_id
                const familyRes = await fetch(`${API_URL}/user/load_user_family?vk_id=${vkId}`);
                const familyData = await familyRes.json();
                
                if (familyData.status === 'family_found') {
                    const familyId = familyData.family_id;
                    
                    // Загружаем участников семьи
                    // В logic API нет прямого метода, но можно использовать members router
                    const membersRes = await fetch(`${API_URL}/members/family/${familyId}`);
                    const members = await membersRes.json();
                    
                    const select = document.getElementById('executor-select');
                    
                    // Добавляем членов семьи (кроме текущего пользователя, так как "Я" уже есть)
                    members.forEach(member => {
                        if (member.user_id != currentUserId) {
                            const option = document.createElement('option');
                            option.value = member.user_id;
                            option.textContent = member.name;
                            select.appendChild(option);
                        }
                    });
                }
            } catch (e) {
                console.error('Не удалось загрузить членов семьи:', e);
            }
        }
