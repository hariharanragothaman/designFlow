import redis
connection = redis.Redis()

topics = ["boston", "newyork"]

subscribe = connection.pubsub()
subscribe.subscribe(topics)

for message in subscribe.listen():
    print(message)