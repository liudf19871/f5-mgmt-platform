from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, devices, clusters, monitor, config, logs, reports, batch, users, audit
from app.core.init_db import init_db

init_db()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(clusters.router, prefix="/api/clusters", tags=["clusters"])
app.include_router(monitor.router, prefix="/api/monitor", tags=["monitor"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(batch.router, prefix="/api/batch", tags=["batch"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])

@app.get("/")
async def root():
    return {"message": "F5 Management Platform API"}