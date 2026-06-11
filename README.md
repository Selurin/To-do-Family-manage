# 🏡 Family Manager | VK Mini App

> **Удобный планировщик семейных задач прямо внутри ВКонтакте.**
> Делегируйте бытовые поручения, отслеживайте статусы и получайте мгновенные уведомления через VK-бота!

🚀 **[Открыть приложение](https://vk.com/app54590248)** | 🤖 **[Сообщество VK-бота](https://vk.com/club238633411)**

---

## 📖 О проекте
**Family Manager** — это веб-приложение, бесшовно встроенное в экосистему ВКонтакте в формате VK Mini App. Оно решает проблему хаоса в семейных делах: кто должен вынести мусор, кому купить продукты и кто забыл полить цветы. 

Приложение позволяет создавать закрытые семейные группы, назначать задачи конкретным участникам, устанавливать дедлайны и автоматически получать уведомления в личные сообщения ВКонтакте, как только появляется новое поручение.

## ✨ Ключевые возможности
* **Быстрая авторизация:** Вход в один клик через профиль ВКонтакте (автоматическое подтягивание имени и аватара).
* **Семейные группы:** Создание семей и приглашение участников по уникальному защищенному коду.
* **Умный список задач:** Фильтры «Мои задачи» / «Все задачи», указание исполнителя и сроков.
* **Мгновенные уведомления:** Фоновый VK-бот автоматически пишет в ЛС, когда вам назначают новое дело.
* **Безопасность:** Защита от SQL-инъекций, валидация данных на фронтенде и бэкенде, хранение токенов в переменных окружения.
* **Ролевая модель:** Разграничение прав (Создатель, Участник и др.).

---

## 🖼️ Возможности интерфейса

### Экран авторизации
<img width="579" height="445" alt="image" src="https://github.com/user-attachments/assets/6e8bd527-775e-4eaf-868c-ab634ccc4cd3" /> 

### Список задач
<img width="569" height="431" alt="image" src="https://github.com/user-attachments/assets/6b9bfb8a-fcdf-40ab-9763-38585de1b21c" />

 ### Уведомление от бота
 <img width="258" height="151" alt="image" src="https://github.com/user-attachments/assets/29f430fa-df59-4cd8-8151-0cced0888bb2" />

---

## Технологический стек

| Направление | Технологии |
| :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) ![FastAPI/Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-teal) |
| **Frontend** | ![Node.js](https://img.shields.io/badge/Node.js-18+-green?logo=node.js) ![HTML/CSS/JS](https://img.shields.io/badge/HTML/CSS/JS-orange) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?logo=postgresql) |
| **Integrations**| ![VK API](https://img.shields.io/badge/VK_API-Mini_Apps_&_Bot-0077FF?logo=vk) |
| **Tools** | Git, pgAdmin 4, dotenv, npm |

---

## Архитектура и принцип работы
Система построена по классической **клиент-серверной архитектуре**:
1. **Frontend (VK Mini App):** Отрисовывает UI, взаимодействует с пользователем, отправляет HTTP-запросы к API.
2. **Backend (Python API):** Обрабатывает запросы, работает с бизнес-логикой, валидирует данные и управляет сессиями.
3. **PostgreSQL:** Реляционное хранилище данных (пользователи, семьи, задачи, статусы).
4. **VK Bot (Background Worker):** Асинхронно опрашивает базу данных на наличие новых задач (`status='new'`, `is_notified=False`), отправляет уведомления пользователям через VK API и обновляет статусы в БД.

---

## Установка и локальный запуск (Для разработчиков)

Если вы хотите развернуть проект локально для разработки или тестирования, выполните следующие шаги.

### 1. Системные требования
* Python 3.10+
* Node.js 18+ & npm
* PostgreSQL 14+
* Свободные порты: `8000` (Backend), `5432` (PostgreSQL), `3000` или `5173` (Frontend)

### 2. Клонирование и настройка Backend
```bash
git clone https://github.com/Selurin/To-do-Family-manage.git
cd family-manager

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt
```
### 3. Конфигурация переменных окружения
Создайте в корне файл `.env` и заполните его своими данными:
```env
# VK API Integration
VK_TOKEN=vk1.a.ваш_секретный_токен_сообщества
VK_GROUP_ID=ваш_id_сообщества

# Database
DB_DSN=postgres://postgres:ваш_пароль@localhost:5432/family_manager

# Dev Mode
DEV_PASSWORD=ваш_пароль_для_ручного_входа
```

### 4. Подготовка базы данных
Создайте базу данных `family_manager` в PostgreSQL

### 5. Запуск сервера (Backend)
```bash
uvicorn app.main:app --reload
```

### 6. Запуск интерфейса (Frontend)
```bash
npm install
npx serve
```

## 🤝 Участие в разработке
Если вы нашли баг или хотите предложить фичу:
🐛 **[Issues](https://github.com/Selurin/To-do-Family-manage/issues)**
