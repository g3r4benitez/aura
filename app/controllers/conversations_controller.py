from fastapi import APIRouter, Depends

from app.entities.conversations import ConversationsFilterDTO
from app.services.conversation_service import conversation_service

router = APIRouter()


@router.api_route("/conversations", methods=["GET"])
async def get_conversations(params: ConversationsFilterDTO = Depends() ):
    conversations = conversation_service.filter(params)
    return conversations