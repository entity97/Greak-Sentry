"""Start Greak Sentry.

On your PC:   python main.py
In Docker:    docker compose up -d
"""

import logging
import os

from sentry.config import load_settings
from sentry.core import Sentry

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    Sentry(load_settings()).run()
