from fastapi import FastAPI

from app.routes import auth, users, wallets, categories
from app.database.init_db import init_db

init_db()
app = FastAPI(title="Asset Management API", version="0.0.0")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(wallets.router, prefix="/wallets", tags=["Wallets"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
