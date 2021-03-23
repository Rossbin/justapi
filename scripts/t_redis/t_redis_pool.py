#redis连接池
import redis
#pool必须是单例的
POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,max_connections=100)  # 造一个池子,最多能放100个连接