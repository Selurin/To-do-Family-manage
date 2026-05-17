 const API_URL = 'https://todo-stasnau.amvera.io';
        let allTasks = [];
        let currentUserId = null;
        let currentTab = 'my';

        // Инициализация
        document.addEventListener('DOMContentLoaded', async () => {
            const storedId = localStorage.getItem('user_id');
            const storedVk = localStorage.getItem('vk_id');
            
            if (!storedId || !storedVk) {
                window.location.href = 'index.html';
                return;
            }
            currentUserId = parseInt(storedId);
            
            await loadTasks();
        });

        // Загрузка задач (1 запрос -> готовые данные)
        async function loadTasks() {
            const container = document.getElementById('tasks-container');
            container.innerHTML = '<div style="color:white; text-align:center; padding:20px;"> Загрузка задач...</div>';

            try {
                const res = await fetch(`${API_URL}/task/get_family_tasks?user_id=${currentUserId}`);
                const data = await res.json();

                if (data.status?.startsWith('ERR')) {
                    container.innerHTML = `<div style="color:#ff6b6b; text-align:center; padding:20px;">❌ ${data.status}</div>`;
                    return;
                }

                allTasks = data.tasks || [];
                renderTasks();
            } catch (e) {
                console.error(e);
                container.innerHTML = '<div style="color:#ff6b6b; text-align:center; padding:20px;">Нет связи с сервером</div>';
            }
        }

        //Переключение табов
        function switchTab(tab) {
            currentTab = tab;
            document.getElementById('tab-my').className = tab === 'my' ? 'tab-btn active' : 'tab-btn';
            document.getElementById('tab-all').className = tab === 'all' ? 'tab-btn active' : 'tab-btn';
            renderTasks();
        }

        // Отрисовка карточек
        function renderTasks() {
            const container = document.getElementById('tasks-container');
            container.innerHTML = '';

            // Фильтрация по табу
            const filtered = currentTab === 'my' 
                ? allTasks.filter(t => t.assigned_to_id === currentUserId)
                : allTasks;

            if (filtered.length === 0) {
                container.innerHTML = '<div style="color:white; text-align:center; padding:20px;"> Задач пока нет</div>';
                return;
            }

            filtered.forEach(task => {
                const isDone = task.status === 'done';
                const html = `
                    <div class="task-item ${isDone ? 'completed' : ''}">
                        <input type="checkbox" class="task-checkbox" ${isDone ? 'checked' : ''} 
                               onchange="handleDelete(event, ${task.task_id})">
                        <div class="task-content">
                            <div class="task-title">${escapeHtml(task.title)}</div>
                            <div class="task-assignee">
                                Кому: ${escapeHtml(task.assignee_name)} | От: ${escapeHtml(task.creator_name)}
                            </div>
                        </div>
                    </div>
                `;
                container.innerHTML += html;
            });
        }

        // Удаление задачи по чекбоксу
        function handleDelete(event, taskId) {
            event.stopPropagation();
            if (!confirm('Удалить эту задачу?')) {
                event.target.checked = !event.target.checked;
                return;
            }

            fetch(`${API_URL}/task/delete_task?task_id=${taskId}`, { method: 'POST' })
                .then(() => {
                    allTasks = allTasks.filter(t => t.task_id !== taskId);
                    renderTasks();
                })
                .catch(() => alert('Ошибка при удалении'));
        }

        // Защита от XSS при выводе текста
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
