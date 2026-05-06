import asyncpg
from .config import DB_DSN
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

db = Database(DB_DSN)
