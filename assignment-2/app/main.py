from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncpg
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/users", response_class=HTMLResponse)
async def get_users_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/api/users")
async def get_users():
    try:
        async with app.state.db.acquire() as conn:
            rows = await conn.fetch("SELECT username FROM users LIMIT 10")
            users = [row["username"] for row in rows]
            return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        async with app.state.db.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE username=$1 AND password=$2", username, password)
            if row:
                return JSONResponse(content={"message": "Login successful"})
            else:
                return JSONResponse(content={"message": "Login failed"}, status_code=401)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")
