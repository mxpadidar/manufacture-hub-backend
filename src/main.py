from auth.routes import router as auth_router
from fastapi import FastAPI

from account.routes import router as accounts_router

app = FastAPI()
app.include_router(accounts_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
