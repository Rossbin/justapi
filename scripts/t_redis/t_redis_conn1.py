

# 简单使用
from redis import Redis
conn=Redis(host='127.0.0.1', port=6379,decode_responses=True)
conn.lpush('list1',999)