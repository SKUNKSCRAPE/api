from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.bootstrap import bootstrap_admin_user
from app.db.session import Base, engine
from app.routers import auth, jobs, results

Base.metadata.create_all(bind=engine)
bootstrap_admin_user()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix, tags=["auth"])
app.include_router(jobs.router, prefix=settings.api_v1_prefix, tags=["jobs"])
app.include_router(results.router, prefix=settings.api_v1_prefix, tags=["results"])


@app.get("/healthz", summary="Health check")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
