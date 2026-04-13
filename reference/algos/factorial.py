def factorial(num):
    res = num
    while num > 1:
        res = res * (num-1)
        num -= 1

    return res

def factorial(num):
    res = 1
    for i in range(1, num+1):
        res = res * i

    return res

def factorial_rec(num):
    if num == 1:
        return num
    else:
        return num * factorial_rec(num - 1)


print(factorial(5))
# print(factorial_rec(5))