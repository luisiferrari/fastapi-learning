from redis.asyncio import Redis as redis
from src.config import Config

JTI_EXPIRE = 3600

redis_token_block_list = redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    await redis_token_block_list.set(
        name=jti,
        value='revoked',
        ex=JTI_EXPIRE
    )
    
async def token_in_blocklist(jti: str) -> bool:
    jti = await redis_token_block_list.get(jti)
    return jti is not None