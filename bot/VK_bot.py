import os
import time
import threading
import psycopg2
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkApi
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('VK_TOKEN')
GROUP_ID = int(os.getenv('VK_GROUP_ID'))

# Строка подключения к БД (из вашего config.py)
DB_DSN = os.getenv(
    "DB_DSN",
    "postgres://postgres:1z9x8c7v@localhost:5432/family_manager"
)

# Инициализация ВК
vk_session = VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# Множество для хранения ID уже отправленных задач
sent_tasks = set()

def check_new_tasks():
    """Проверяет новые задачи и отправляет уведомления"""
    global sent_tasks
    print("🔍 Проверка БД...")

    try:
        conn = psycopg2.connect(DB_DSN)
        cursor = conn.cursor()

        # Получаем задачи с JOIN на users для назначенного и для создателя
        cursor.execute("""
            SELECT 
                t.id, 
                t.title, 
                t.description, 
                t.deadline,
                assigned_user.vk_id as assigned_vk_id,
                creator_user.name as creator_name
            FROM tasks t
            JOIN users assigned_user ON t.assigned_to = assigned_user.id
            JOIN users creator_user ON t.creator_id = creator_user.id
            WHERE t.notification_sent = FALSE
            ORDER BY t.id ASC
        """)

        tasks = cursor.fetchall()
        print(f"📊 Найдено неотправленных задач: {len(tasks)}")

        for task in tasks:
            task_id = task[0]
            title = task[1]
            description = task[2]
            deadline = task[3]
            vk_user_id = task[4]  # ← VK ID назначенного
            creator_name = task[5]  # ← Имя создателя!

            # Пропускаем уже обработанные
            if task_id in sent_tasks:
                continue

            # Формируем сообщение (теперь с именем создателя)
            message = f"📋 Новая задача!\n\n"
            message += f"{title}\n\n"
            if description:
                message += f"{description}\n\n"
            if deadline:
                message += f"⏰ Дедлайн: {deadline.strftime('%d.%m.%Y %H:%M')}\n"
            message += f"\n👤 Создатель: {creator_name}"  # ← теперь имя, а не ID

            # Отправляем уведомление
            try:
                vk.messages.send(
                    peer_id=vk_user_id,
                    message=message,
                    random_id=0
                )
                print(
                    f"✅ Уведомление отправлено пользователю {vk_user_id} о задаче #{task_id}: {title} (создатель: {creator_name})")

                # Помечаем как отправленное
                cursor.execute(
                    "UPDATE tasks SET notification_sent = TRUE WHERE id = %s",
                    (task_id,)
                )
                conn.commit()

                sent_tasks.add(task_id)

            except Exception as e:
                print(f"❌ Ошибка отправки задачи #{task_id}: {e}")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"❌ Ошибка БД: {e}")


def monitor_tasks():
    """Фоновый мониторинг таблицы tasks"""
    print("🔄 Мониторинг задач запущен (проверка каждые 5 секунд)")
    while True:
        check_new_tasks()
        time.sleep(5)


def main():
    print("=" * 50)
    print("✅ Бот-монитор задач ВК запущен!")
    print(f"📁 Отслеживается таблица: tasks")
    print(f"👥 Группа ВК ID: {GROUP_ID}")
    print("=" * 50)

    # Запускаем мониторинг в фоновом потоке
    monitor_thread = threading.Thread(target=monitor_tasks, daemon=True)
    monitor_thread.start()

    # Основной цикл для команд
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            text = message['text'].lower()
            user_id = message['from_id']

            # Обработка кнопки "Начать"
            if text == 'начать':
                vk.messages.send(
                    peer_id=user_id,
                    message="👋 Привет! Я бот семьи.\n\n"
                            "📌 Я буду уведомлять вас о новых задачах.\n"
                            "💡 Команды: /status и /help",
                    random_id=0
                )

            if text == '/status':
                vk.messages.send(
                    peer_id=user_id,
                    message="🤖 Бот работает и отслеживает новые задачи.\n\n"
                            "Новые задачи приходят автоматически при создании.",
                    random_id=0
                )
            elif text == '/help':
                vk.messages.send(
                    peer_id=user_id,
                    message="🤖 Доступные команды:\n\n"
                            "/status - статус бота\n"
                            "/help - это сообщение\n\n"
                            "📌 Бот автоматически уведомляет о новых задачах",
                    random_id=0
                )


if __name__ == '__main__':
    main()