from fastapi import APIRouter
from app.services.statistic_service import statistic_service

router = APIRouter()


@router.api_route("/", methods=["GET"])
async def get_statistics():
    statistics = statistic_service.get_all()
    return statistics

