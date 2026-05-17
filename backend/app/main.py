from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import DB_DSN
from database import Database, db
from fastapi.middleware.cors import CORSMiddleware
from logic import user_router, family_router, task_router, members_router
from routes.devpassword import router as devpassword_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield  # <- приложение работает здесь
    await db.close()

app = FastAPI(title="Family Manager Backend", lifespan=lifespan)

# Этот блок должен быть именно здесь!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешает запросы с любого адреса (включая твой Live Server)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(family_router.router)
app.include_router(task_router.router)
app.include_router(members_router.router)
app.include_router(devpassword_router)
