from src.utils.redis_manager import RedisManager
from src.config import settings

redis_manager = RedisManager(redis_url=settings.REDIS_URL)
