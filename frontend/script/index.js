vkMainBtn.addEventListener('click', async () => {
    console.log("Клик по кнопке ВК зафиксирован. Запрашиваем VKWebAppGetUserInfo...");
    try {
        // 1. Получаем данные пользователя из ВК
        const vkData = await vkBridge.send('VKWebAppGetUserInfo');
        console.log('Данные от ВК получены успешно:', vkData);

        // САМОЕ ВАЖНОЕ: Сохраняем ID моментально, до любых запросов на бэкенд!
        localStorage.setItem('vk_id', vkData.id);
        localStorage.setItem('vk_user_id', vkData.id);
        localStorage.setItem('user_id', vkData.id);
        localStorage.setItem('user_name', `${vkData.first_name} ${vkData.last_name}`.trim());

        // 2. Отправляем запрос на бэкенд (оставляем как у тебя)
        console.log('Отправляем запрос на бэкенд:', `${API_URL}/check-password`);
        const response = await fetch(`${API_URL}/check-password`, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                vk_id: vkData.id,
                first_name: vkData.first_name,
                last_name: vkData.last_name,
                photo: vkData.photo_200,
                launch_params: window.location.search 
            })
        });

        // 3. Регистрируем пользователя в БД
        console.log('Регистрируем пользователя на бэкенде...');
        const fullName = `${vkData.first_name} ${vkData.last_name}`.trim();
        const regRes = await fetch(`${API_URL}/user/register?vk_id=${vkData.id}&name=${encodeURIComponent(fullName)}`, { 
            method: 'POST' 
        });
        const regData = await regRes.json();
        console.log('Ответ от бэкенда user/register:', regData);

        // 4. Проверяем, состоит ли пользователь в семье
        try {
            const famRes = await fetch(`${API_URL}/user/load_user_family?vk_id=${vkData.id}`);
            const famData = await famRes.json();
            const famStatus = getField(famData, 'status')?.trim();

            if (famStatus === 'family_found') {
                const familyId = getField(famData, 'family_id');
                localStorage.setItem('family_id', familyId);
                console.log('Семья найдена. Перенаправление на tasks.html');
                window.location.href = 'tasks.html';
            } else {
                console.log('Семья не найдена. Перенаправление на choose.html');
                window.location.href = 'choose.html';
            }
        } catch (famErr) {
            console.warn('Не удалось проверить семью, переход на choose.html', famErr);
            window.location.href = 'choose.html';
        }

    } catch (error) {
        console.error('Ошибка в процессе авторизации VK Bridge:', error);
        alert('Вход через ВК был отменен или произошел сбой.');
    }
});
