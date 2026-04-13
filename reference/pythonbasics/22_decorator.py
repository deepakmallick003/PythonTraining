def div(a, b):
    print(a / b)

def smart_div(func):
    def inner(a, b):
        if a < b: a, b = b, a  # Ensures a is always greater than b
        return func(a, b)
    return inner

div = smart_div(div)  # Decorating 'div' function
div(2, 4)  # Using the decorated function
