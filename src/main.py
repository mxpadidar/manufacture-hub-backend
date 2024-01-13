from fastapi import FastAPI

from accounts.routes import router as accounts_router

app = FastAPI()
app.include_router(accounts_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
