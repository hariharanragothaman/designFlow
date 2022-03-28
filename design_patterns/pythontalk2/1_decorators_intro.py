"""
Decorators are also called as higher order functions.
 - They can one or more functions as argments and return a function as its result.
 - They will extend the functions behavior while not modifying the function itself.

There have been 2 decorators since python 2.2
@classmethod
@staticmethod
"""

def doubler(number) -> int:
	""" Function that doubles a value passed to it """
	return number * 2

# Remember functions are first-class objects.
# functions can be passed around and used as arguments - as other data-types such as string / integer.

print(doubler)
print(dir(doubler))


# Create a function that accepts another function as it's argument
def info(func):
	def wrapper(*args):
		print(f"Function name: {func.__name__}")
		return func(*args)
	return wrapper

print("---------------------------")
my_decorator = info(doubler) # Creating object of the function decorator - Remember functions are first class objects.
print(my_decorator(2))
# Well this is how raw-style decorators are created

# Now let's look at how to write decorators in pythonic fashion
@info
def tripler(number):
	""" Functions that triples a number """
	return number * 3

print("---------------------------")
print(tripler(7))

# Now let's look at how decorators can be used otherwise

def bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper
def italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@bold
@italic
def formatted_text():
    return 'Python rocks!'

print("---------------------------")
print(formatted_text())


