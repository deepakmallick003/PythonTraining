def fibo_max_count(maxcount):
    if maxcount > 0:
        num1 = 0
        num2 = 1
        for i in range(maxcount):
            print(num1)
            sum = num1 + num2
            num1 = num2
            num2 = sum
def fibo_maxcount_rec(maxcount, num1=0, num2=1):
    if maxcount <= 0:
        return

    print(num1)

    sum = num1 + num2
    maxcount -= 1
    fibo_maxcount_rec(maxcount, num1=num2, num2=sum)

def fibo_max_num(maxnum):
    num1 = sum = 0
    num2 = 1
    while num1 < maxnum:
        print(num1)
        sum = num1 + num2
        num1 = num2
        num2 = sum

fibo_max_count(10)
fibo_maxcount_rec(10)
fibo_max_num(100)