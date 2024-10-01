from fastapi import APIRouter

from app.controllers import ping_controller as ping
from app.controllers import conversations_controller as conversations
from app.controllers import statistic_controller as statistic
from app.controllers import proxy_controller as proxy
from app.core.config import API_PREFIX

api_router = APIRouter(prefix=API_PREFIX)
api_router.include_router(ping.router, tags=["ping"], prefix="/api/ping")
api_router.include_router(conversations.router, tags=["conversations"], prefix="/api/conversations")
api_router.include_router(statistic.router, tags=["statistics"], prefix="/api/statistics")
api_router.include_router(proxy.router, tags=["proxy"], prefix="")

