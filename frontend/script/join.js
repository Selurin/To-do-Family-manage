const API_URL = 'https://todo-stasnau.amvera.io';

        document.addEventListener('DOMContentLoaded', () => {
            const userId = localStorage.getItem('user_id');
            
            if (!userId) {
                window.location.href = 'index.html';
                return;
            }

            document.getElementById('join-btn').addEventListener('click', async () => {
                const codeInput = document.getElementById('invite-code-input');
                const errorDiv = document.getElementById('join-error');
                const inviteCode = codeInput.value.trim();

                if (errorDiv) {
                    errorDiv.textContent = '';
                }

                if (!inviteCode) {
                    errorDiv.textContent = 'Введите код приглашения!';
                    return;
                }

                try {
                    const res = await fetch(`${API_URL}/family/join?invite_code=${inviteCode}&user_id=${userId}`, {
                        method: 'POST'
                    });
                    const data = await res.json();

                    if (data.status === 'member added') {
                        console.log('Успешный join', data);
                        console.log('family_id из ответа:', data.family_id);
                        // Сохраняем код семьи
                        localStorage.setItem('invite_code', inviteCode);
                        localStorage.setItem('user_id', userId);
                        localStorage.setItem('family_id', data.family_id); 
                        
                        window.location.href = 'joined.html';
                    } else if (data.status === 'ERR: user is already in this family') {
                        errorDiv.textContent = 'Вы уже состоите в этой семье';
                    } else if (data.status === 'ERR: user is in another family') {
                        errorDiv.textContent = 'Вы уже состоите в другой семье';
                    } else {
                        errorDiv.textContent = 'Неверный код приглашения';
                    }
                } catch (e) {
                    errorDiv.textContent = 'Нет связи с сервером';
                    console.error(e);
                }
                
            });
        });
