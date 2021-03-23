

# 简单使用
from redis import Redis
# conn=Redis()
#
# conn=Redis.from_url('redis://127.0.0.1:6379/2')  # 为什么要写成类的绑定方法
#连接对象
# conn=Redis(host='127.0.0.1', port=6379,decode_responses=True)
# ret=conn.get('name')
# print(ret)


# #redis连接池
import redis
# #pool必须是单例的
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379,max_connections=100)  # 造一个池子,最多能放100个连接
# import redis
#
# #包内的py文件，如果想右键运行，导包的时候不能带点
from t_redis_pool import POOL  # pycharm提示的错
conn = redis.Redis(connection_pool=POOL)  # 只要执行这一句话，就是从池中拿出一个连接
# r = redis.Redis(connection_pool=POOL)  # 只要执行这一句话，就是从池中拿出一个连接
# r = redis.Redis(connection_pool=POOL)  # 只要执行这一句话，就是从池中拿出一个连接
# r = redis.Redis(connection_pool=POOL)  # 只要执行这一句话，就是从池中拿出一个连接
# ret=r.get('name')
# print(ret)


#####字符串操作
####1 set的用法
# conn.set('height',180) #基本使用

# conn.set('height','190',nx=True)
# conn.set('height','190',xx=True)
# conn.set('height1','190',xx=True)
'''
ex，过期时间（秒）
     px，过期时间（毫秒）
     nx，如果设置为True，则只有name不存在时，当前set操作才执行,值存在，就修改不了，执行没效果
     xx，如果设置为True，则只有name存在时，当前set操作才执行，值存在才能修改，值不存在，不会设置新值
 
'''

### 2
# setnx(name, value)
#
# 设置值，只有name不存在时，执行设置操作（添加）,如果存在，不会修改
# setex(name, value, time)
# # 设置值
# # 参数：
#     # time，过期时间（数字秒 或 timedelta对象）
# psetex(name, time_ms, value)
# # 设置值
# # 参数：
#     # time_ms，过期时间（数字毫秒 或 timedelta对象


# mset
# conn.mset({'name1':'11','name3':'dasfd'})

# ret=conn.mget(['name1','name','name3'])
# print(ret)

# ret=conn.getset('name1', '999')
# print(ret)

# ret=conn.getrange('name1',0,0) # 前闭后闭区间
# print(ret)

# conn.setrange('name1',1,88888)

# ret=conn.getbit('name1',9)
# print(ret)

#incr ：统计网站访问量，页面访问量，接口访问量
# conn.incr('name1')  # 只要一执行，数字加1
# conn.incr('name1')  # 只要一执行，数字加1
# conn.incr('name1')  # 只要一执行，数字加1
# conn.incr('name1')  # 只要一执行，数字加1

#decr
# conn.incr('name1',-2)
# conn.decr('name1',3)

# conn.append('name1','oo')
# conn.incr('name1')


#set :很多参数
#get
#mset
#mget
#incr
#decr
#append



# hash操作
# conn.hset('hash1','name','lqz')
# conn.hset('hash1','name2','lqz')
# conn.hset('hash1','name','lqz444')  # key不可以重复，

# ret=conn.hget('hash1','name')  #只能取一个
# print(ret)


# conn.hmset('hash2',{'key1':'value1','key2':'value2'})
# ret=conn.hmget('hash1','name','name2')
# ret=conn.hmget('hash1',['name','name2'])
# print(ret)

# ret=conn.hgetall('hash1')  # 尽量少用
# print(ret)

# ret=conn.hlen('hash1')
# ret=conn.hkeys('hash1')
# ret=conn.hexists('hash1','name1')
# ret=conn.hdel('hash1','name')

# conn.hset('hash1','name',12)
# ret=conn.hincrby('hash1','name')
#
# print(ret)


# 以后想取出hash类型内所有的数据，不建议用hgetall，建议用hscan_iter
# 一次性先取一部分回来（假设有1w条，先取回100条，把这100条做成了生成器）
# ret=conn.hscan_iter('hash1')
# print(ret)
# for i in ret:
#     print(i)


# hset
# hget
#hmset
#hmget
# hincrby
# 区分hgetall和hscan_iter

### 列表操作
# ret=conn.lpush('list1',1,2,3,4,5)
# ret=conn.rpush('list1',999)
# ret=conn.lpushx('list2',1)

# ret=conn.lpushx('list1',888)  # 必须有这个key才能放
# ret=conn.rpushx('list1',666)  # 我们猜，返回总长度
# ret=conn.llen('list1')

# ret=conn.linsert('list1','before','3','77777777')
# ret=conn.linsert('list1','after','3','66666666')



# ret=conn.lset('list1',3,'22222')  #从0开始计数
# ret=conn.lset('list1',0,'11111')

# ret=conn.lrem('list1',2,'5')  # 从前往后删除两个5
# ret=conn.lrem('list1',-1,'5') # 从后往前删除1个5
# ret=conn.lrem('list1',0,'5')   # 删除所有5

# ret=conn.lpop('list1')
# ret=conn.rpop('list1')

# ret=conn.lindex('list1',0)

# ret=conn.lrange('list1',0,2)  # 前闭后闭

# ret=conn.ltrim('list1',1,2)

# 重点block,阻塞,可以写一个超时时间
# ret=conn.blpop('list1',timeout=10)
# print(ret)


# 自定制分批取列表的数据
# conn.lpush('test',*[1,2,3,4,45,5,6,7,7,8,43,5,6,768,89,9,65,4,23,54,6757,8,68])
# conn.flushall()
# def scan_list(name,count=2):
#     index=0
#     while True:
#         data_list=conn.lrange(name,index,count+index-1)
#         if not data_list:
#             return
#         index+=count
#         for item in data_list:
#             yield item
# # print(conn.lrange('test',0,100))
# for item in scan_list('test',5):
#     print('---')
#     print(item)



# 管道。实现事务
# import redis
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
#
# conn = redis.Redis(connection_pool=pool)
#
# # pipe = r.pipeline(transaction=False)
# pipe = conn.pipeline(transaction=True)
# pipe.multi()
# pipe.set('name', 'alex')
#
# pipe.set('role', 'sb')
#
# pipe.execute()  # 这句话，才真正的去执行

# 其他操作
# conn.delete('list1')
# ret=conn.delete('hash1')

# ret=conn.exists('hash2')
# ret=conn.keys('cache*')  #查询以cache开头的所有key

# ret=conn.expire('hash2',2)

# ret=conn.type('name3')
# ret=conn.type('test')
# ret=conn.type('test')
# print(ret)