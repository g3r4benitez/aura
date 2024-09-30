import os

from starlette.config import Config

ROOT_DIR = os.getcwd()
_config = Config(os.path.join(ROOT_DIR, ".env"))
APP_VERSION = "0.0.1"
APP_NAME = "TEST PYTHON AURA"
API_PREFIX = ""

# Env vars
IS_DEBUG: bool = _config("IS_DEBUG", cast=bool, default=False)
DB_URL: str = _config("DB_URL", cast=str, default="sqlite:///./app/sql_app.db")

EXTERNAL_API_URL: str = _config("EXTERNAL_API_URL", cast=str, default="http://cualquierapi.com")
CONNECTION_TIMEOUT = _config("CONNECTION_TIMEOUT", cast=int, default=10)