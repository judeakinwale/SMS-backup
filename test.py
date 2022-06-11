def decorator(f):
    print(f"inside decorator body with decorated function {f.__name__}")
    print(f)
    def wrapped(*args, **kwargs):
        print(f"inside inner wrapper function with args: {args} and kwargs: {kwargs}")
        result = f(*args)  # calling the function
        print(result)
        return result

    return wrapped


@decorator
def my_funcion(a, b, c):
    # print("inside my_funcion()")
    summation = sum([a,b,c])
    # print (summation)
    return summation


@decorator
def my_funcion_no_call(a, b, c):
    print("inside my_funcion_no_call()")


print("finished decorating my_funcion()")
my_funcion(1, 2, 3)
print("immediately after my_function() line")