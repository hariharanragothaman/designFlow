"""
What are the questions we want to ask?
# Let's go over the constraints and assumptions
"""
"""
Q1 - For simplicity: Are the keys the integers only? - YES
Q2 - For collision resolution - What's our strategy? - Chaining
Q3 - Do we have to worry about load factors? - No
Q4 - Can we assume I/P's are valid? - Yes - We can assume they are valid
Q5 - Can we assume this fits memory? - YES
"""


class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, size) -> None:
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key) -> int:
        hash_index = key % self.size
        return hash_index

    def set(self, key, value) -> None:
        hash_index = self._hash_function(key)
        for item in self.table[hash_index]:
            if item.key == key:
                item.value = value
                return
        self.table[hash_index].append(Item(key, value))

    def get(self, key):
        hash_index = self._hash_function(key)
        for item in self.table[hash_index]:
            if item.key == key:
                return item.value
        raise KeyError('Key not found in hashmap')

    def remove(self, key):
        hash_index = self._hash_function(key)
        for index, item in enumerate(self.table[hash_index]):
            if item.key == key:
                del self.table[hash_index][index]
        raise KeyError('Key not Present in hashmap')