def info(arg1, arg2):
    print('Decorator arg1 = ' + str(arg1))
    print('Decorator arg2 = ' + str(arg2))

    def the_real_decorator(function):

        def wrapper(*args, **kwargs):
            print('Function {} args: {} kwargs: {}'.format(
                function.__name__, str(args), str(kwargs)))
            return function(*args, **kwargs)

        return wrapper

    return the_real_decorator

def doubler(number):
    return number * 2

decorator_function = info(3, 'Python')
print(decorator_function)

actual_decorator = decorator_function(doubler)
print(actual_decorator)

# Call the decorated function
print(actual_decorator(5))