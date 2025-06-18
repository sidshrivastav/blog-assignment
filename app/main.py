from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.v1.endpoints import blog, auth
from app.db.base import Base
from app.db.session import engine
from app.middleware.access_log import AccessLogMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with SQLite")
app.add_middleware(AccessLogMiddleware)

app.include_router(blog.router, prefix="/api/v1/blog", tags=["Blog"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])


@app.get("/log-dashboard", response_class=HTMLResponse)
def log_dashboard():
    log_content = Path("logs/access.log").read_text(encoding="utf-8")[-10000:]  # Read last 10k chars
    html = f"""
    <html>
        <head><title>Log Dashboard</title></head>
        <body style="font-family: monospace; white-space: pre-wrap; background: #111; color: #eee; padding: 1rem;">
            <h2>Access Logs</h2>
            <div>{log_content.replace('\n', '<br>')}</div>
        </body>
    </html>
    """
    return html
