from loguru import logger
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "access.log"

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
)

# File sink for dashboard viewing
logger.add(
    LOG_FILE,
    rotation="10 MB",      # Rotate after 10MB
    retention="7 days",    # Keep logs for 7 days
    enqueue=True,
    backtrace=True,
    diagnose=True,
    level="INFO",
)
