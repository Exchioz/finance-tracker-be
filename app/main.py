from fastapi import FastAPI

from app.routes import users
from app.database.init_db import init_db

init_db()
app = FastAPI(title="Asset Management API", version="0.0.0")

app.include_router(users.router, prefix="/users", tags=["Users"])