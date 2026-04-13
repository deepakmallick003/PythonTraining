def gcd_division(a, b):
    while b != 0:
        remainder = a % b
        print(f"{a} = {a//b} * {b} + {remainder}")
        a = b
        b = remainder
    return a

a = 60
b = 36
print("The Euclidean algorithm using division:\n")
print(f"The GCD of {a} and {b} is: {gcd_division(a, b)}")