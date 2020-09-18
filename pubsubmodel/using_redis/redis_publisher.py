import redis

def publish():
    connection = redis.Redis()
    cities = ["boston", "newyork", "toronto",]
    names = ["elizabeth", "scarlett", 'anne']
    hmap = dict(zip(cities,  names))
    print(hmap)
    for key, value in hmap.items():
        connection.publish(key, value)


if __name__ == '__main__':
    publish()