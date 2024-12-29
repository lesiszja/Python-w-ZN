def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        func(*args, **kwargs)
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def function(x, y, z):
    print("Hello from function: ", x, y, z)

function(1, 2, 3)