from redis import Redis

session_storage = Redis(
    host = "redis", 
    port = 6379, 
    db = 0,
    decode_responses = True
)

cache_storage = Redis(
    host = "redis",
    port = 6379,
    db = 1,
    decode_responses = True
)