from fastapi import APIRouter

from app.controllers import proxy_controller as proxy
from app.controllers import ping_controller as ping
from app.core.config import API_PREFIX

api_router = APIRouter(prefix=API_PREFIX)
api_router.include_router(proxy.router, tags=["proxy"], prefix="/categories")
api_router.include_router(ping.router, tags=["ping"], prefix="/api/ping")
