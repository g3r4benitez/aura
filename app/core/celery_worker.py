from datetime import timedelta
from celery.utils.log import get_task_logger

from .celery_app import celery_app
from app.models.statistic import Statistic
from app.services.statistic_service import statistic_service
from .logger import logger

celery_log = get_task_logger(__name__)

@celery_app.task(
    name='app.core.celery_worker.save_statistic_task'
)
def save_statistic_task(path: str, status_code: int, seconds: float):
    statistic = Statistic()
    statistic.path = path
    statistic.status_code = status_code
    statistic.seconds = seconds
    statistic_service.create(statistic)
