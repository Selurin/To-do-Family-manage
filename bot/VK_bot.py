import os
import time
import threading
import vk_api
import psycopg2
from psycopg2.extras import RealDictCursor

# 1. Загружаем переменные окружения из панели Amvera
TOKEN = os.getenv('VK_TOKEN')
DB_DSN = os.getenv('DB_DSN')  # Убедись, что в настройках Amvera бота есть переменная DB_DSN с адресом твоей БД

if not TOKEN or not DB_DSN:
    raise ValueError("❌ Критические переменные окружения (VK_TOKEN или DB_DSN) не найдены!")

# 2. Инициализация ВК сессии
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


def check_database_for_new_tasks():
    """Фоновая функция, которая мониторит появление новых задач в БД"""
    print("🚀 Фоновый мониторинг базы данных успешно запущен...")

    while True:
        conn = None
        try:
            # Подключаемся к PostgreSQL (используем RealDictCursor, чтобы обращаться к полям по именам)
            conn = psycopg2.connect(DB_DSN, cursor_factory=RealDictCursor)
            cur = conn.cursor()

            # Связываем таблицу задач с таблицей пользователей, чтобы узнать vk_id исполнителя (assigned_to)
            # Также берем имя создателя задачи (creator_id)
            cur.execute("""
                SELECT 
                    t.id AS task_id, 
                    t.title AS task_title, 
                    u.vk_id AS executor_vk_id, 
                    c.name AS creator_name
                FROM tasks t
                JOIN users u ON t.assigned_to = u.id
                LEFT JOIN users c ON t.creator_id = c.id
                WHERE t.is_notified = FALSE AND t.status = 'new';
            """)

            new_tasks = cur.fetchall()

            for task in new_tasks:
                t_id = task['task_id']
                title = task['task_title']
                vk_id = task['executor_vk_id']
                creator = task['creator_name'] or "Участник семьи"

                try:
                    # Отправляем сообщение исполнителю в ВК
                    message_text = (
                        f"🔔 **Новая задача для тебя!**\n\n"
                        f"📌 **Что сделать:** {title}\n"
                        f"👤 **Поручил:** {creator}\n\n"
                        f"Удачи в выполнении! 💪"
                    )

                    vk.messages.send(
                        user_id=vk_id,
                        message=message_text,
                        random_id=0
                    )
                    print(f"✅ Уведомление по задаче №{t_id} успешно отправлено пользователю VK ID: {vk_id}")

                    # Замечаем в БД, что уведомление успешно ушло
                    cur.execute("UPDATE tasks SET is_notified = TRUE WHERE id = %s;", (t_id,))
                    conn.commit()

                except vk_api.exceptions.ApiError as vk_err:
                    print(f"❌ Не удалось отправить сообщение в ВК для {vk_id}. Ошибка: {vk_err}")
                    # Если пользователь заблокировал бота или не написал ему первым,
                    # всё равно ставим TRUE, чтобы бот не зацикливался на этой задаче
                    cur.execute("UPDATE tasks SET is_notified = TRUE WHERE id = %s;", (t_id,))
                    conn.commit()

            cur.close()

        except Exception as e:
            print(f"❌ Ошибка в цикле проверки БД: {e}")

        finally:
            if conn:
                conn.close()

        # Спим 5 секунд перед следующей проверкой базы данных
        time.sleep(5)


if __name__ == "__main__":
    # Запускаем проверку базы данных в отдельном независимом потоке
    monitor_thread = threading.Thread(target=check_database_for_new_tasks, daemon=True)
    monitor_thread.start()

    print("🤖 Бот-уведомитель успешно инициализирован и работает.")

    # Здесь можно оставить стандартный LongPoll, если бот должен отвечать на текстовые сообщения в будущем.
    # Сейчас просто удерживаем главный поток приложения, чтобы контейнер не завершал работу:
    while True:
        time.sleep(1)