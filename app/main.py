"""
FastAPI application entry point.

Assembles routers and initializes the database tables on startup.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import tasks, users


# ---------------------------------------------------------------------------
# Lifespan — runs once at startup / shutdown
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Create all database tables on startup (idempotent)."""
    # Import models so SQLAlchemy registers them with Base.metadata
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    yield


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="A REST API for managing Users and Tasks.",
    lifespan=lifespan,
)

# Mount routers
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def health_check():
    """Simple health-check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
