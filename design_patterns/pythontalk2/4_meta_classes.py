class MyActualClass:
    def __init__(self):
        print('in MyActualClass __init__()')

    def quad(self, value):
        return value * 4

obj = MyActualClass()
print(obj.quad(4))

"""
Now let's say we want to add special functionality to our class without modifying what it already does. 
For example, this might be code that we can't change for backwards compatibility reasons or some other business requirement. Instead, we can decorate it to extend it's functionality.

"""

def decorator(cls):
    class Wrapper(cls):
        def doubler(self, value):
            return value * 2
    return Wrapper

@decorator
class MyActualClass2:
    def __init__(self):
        print('in MyActualClass __init__()')

    def quad(self, value):
        return value * 4

obj = MyActualClass2()
print(obj.quad(4))
print(obj.doubler(5))