import redis

def publish():
    connection = redis.Redis()
    cities = ["boston", "newyork", "toronto",]
    names = ["elizabeth", "scarlett", 'anne']
    hash_map = dict(zip(cities,  names))
    for key, value in hash_map.items():
        connection.publish(key, value)

if __name__ == '__main__':
    publish()