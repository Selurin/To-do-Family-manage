import asyncpg
from config import DB_DSN

class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    # ============================
    # Пользователи
    # ============================

    async def create_user(self, vk_id: int, name: str):
        query = """
        INSERT INTO users (vk_id, name)
        VALUES ($1, $2)
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, vk_id, name)

    async def get_user_by_vk_id(self, vk_id: int):
        query = "SELECT * FROM users WHERE vk_id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, vk_id)

    async def ensure_user_exists(self, user_id: int):
        """
        Автоматически создает запись пользователя, если её еще нет в таблице users.
        Если пользователь уже существует, благодаря ON CONFLICT запрос ничего не ломает.
        """
        query = """
        INSERT INTO users (id, vk_id, name)
        VALUES ($1, $2, $3)
        ON CONFLICT (id) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, user_id, f"Пользователь {user_id}")
            
    async def update_user_name(self, vk_id: int, new_name: str):
        query = "UPDATE users SET name = $1 WHERE vk_id = $2;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, new_name, vk_id)

    # ============================
    # Семьи
    # ============================

    async def create_family(self, name: str, invite_code: str):
        query = """
        INSERT INTO families (name, invite_code)
        VALUES ($1, $2)
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, name, invite_code)

    async def get_family_by_code(self, invite_code: str):
        query = "SELECT * FROM families WHERE invite_code = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, invite_code)
            
    async def get_family_by_id(self, family_id: int):
        query = "SELECT * FROM families WHERE id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, family_id)
            
    # 🔥 ИСПРАВЛЕНИЕ: Новый метод для получения семьи по её ID
    async def get_family_by_id(self, family_id: int):
        query = "SELECT * FROM families WHERE id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, family_id)

    # ============================
    # Участники семьи
    # ============================

    async def add_member(self, user_id: int, family_id: int, role: str):
        query = """
        INSERT INTO family_members (user_id, family_id, role)
        VALUES ($1, $2, $3)
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, user_id, family_id, role)

    async def get_family_members(self, family_id: int):
        query = """
        SELECT fm.*, u.name, u.vk_id
        FROM family_members fm
        JOIN users u ON u.id = fm.user_id
        WHERE fm.family_id = $1;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, family_id)
        
    async def check_membership_by_user_id(self, user_id: int): # Проверка, в какой семье состоит пользователь
        query = """
        SELECT * FROM family_members WHERE user_id = $1;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, user_id)
        
    async def delete_member(self, user_id: int): # Выход из семьи
        query = """
        DELETE FROM family_members WHERE user_id = $1;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id)

    async def change_user_role(self, user_id: int, new_role: str):
        """
        Обновляет роль участника внутри семьи.
        """
        query = """
        UPDATE family_members 
        SET role = $1 
        WHERE user_id = $2;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, new_role, user_id)

    # ============================
    # Задачи
    # ============================

    async def create_task(self, family_id: int, creator_id: int, title: str, description: str = None):
        query = """
        INSERT INTO tasks (family_id, creator_id, title, description, status)
        VALUES ($1, $2, $3, $4, 'new')
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, family_id, creator_id, title, description)

    async def assign_task(self, task_id: int, user_id: int):
        query = "UPDATE tasks SET assigned_to = $1 WHERE id = $2;"
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, task_id)

    async def get_family_tasks(self, family_id: int):
        query = "SELECT * FROM tasks WHERE family_id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, family_id)
        
    async def get_family_task_ids(self, family_id: int): # Получить ID всех задач семьи
        query = "SELECT id FROM tasks WHERE family_id = $1;"
        async with self.pool.acquire() as conn:
            records = await conn.fetch(query, family_id)
            return [record['id'] for record in records]

    async def get_user_task_ids(self, user_id: int): # Получить ID задач пользователя
        query = "SELECT id FROM tasks WHERE assigned_to = $1;"  
        async with self.pool.acquire() as conn:
            records = await conn.fetch(query, user_id)
            return [record['id'] for record in records]
    
    async def get_task_by_title(self, title: str): # Найти задачу по названию
        query = "SELECT * FROM tasks WHERE title = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, title)

    async def get_task_by_id(self, task_id: int): # Получить полную инфо о задаче
        query = "SELECT * FROM tasks WHERE id = $1;"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, task_id)

    async def delete_task(self, task_id: int): # Удалить задачу
        query = """
        DELETE FROM tasks WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, task_id)

    async def get_family_by_invite_code(self, invite_code: str):
        return await self.get_family_by_code(invite_code)
    
    async def close(self):
        if self.pool:
            await self.pool.close()

db = Database(DB_DSN)
