from fastapi import FastAPI
from .config import DB_DSN
from .database import Database, db
from .routes import users, families, tasks, members
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Family Manager Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на время разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

app.include_router(users.router)
app.include_router(families.router)
app.include_router(tasks.router)
app.include_router(members.router)
