from dotenv import load_dotenv
load_dotenv()

import contextlib
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import health, users, posts, wallet, comments
from app.utils.middleware import QAMiddleware
from app.utils.database import engine, Base
from app.utils.scheduler import init_scheduler

@contextlib.asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    init_scheduler()
    yield
    await engine.dispose()

app = FastAPI(title="Yoris API", lifespan=lifespan)

app.add_middleware(QAMiddleware)

app.include_router(health.router)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])

@app.get("/test/error/{status_code}")
async def test_error(status_code: int):
    return JSONResponse(status_code=status_code, content={"error": f"Mocking HTTP {status_code}"})
