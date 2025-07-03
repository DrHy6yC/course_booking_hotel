from src.config import settings
from src.utils.redis_manager import RedisManager

redis_manager = RedisManager(redis_url=settings.redis_url)
