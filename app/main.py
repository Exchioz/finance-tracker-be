from fastapi import FastAPI

from app.routes import users, wallets
from app.database.init_db import init_db

init_db()
app = FastAPI(title="Asset Management API", version="0.0.0")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(wallets.router, prefix="/wallets", tags=["Wallets"])
# app.include_router(assets.router, prefix="/assets", tags=["Assets"])
