import redis
import hashlib

from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def get_key_from_text(plain_text: str):
    return hashlib.md5(f"{plain_text}".encode("utf")).hexdigest()