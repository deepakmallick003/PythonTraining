print()
print("Global Keyword - Question 1")
print("Modify a global variable 'x' inside a function using the global keyword. Expected output: Global x: 15, Outside x: 15")
x = 10
def func():
    global x
    x = 15
    print("Global x:", x)
func()
print('Input:\n x = 10\ndef func():\n    global x\n    x = 15\n    print("Global x:", x)\nfunc()')
print('Output:\n Outside x:', x)
print('-'*20)
print()

print("globals() Function - Question 2")
print("Access and modify a global variable 'x' inside a function in the presence of a local variable with the same name. Expected output: Local x: 15, Global x: 10, Modified Global x: 20")
x = 10
def func():
    x = 15
    print("Local x:", x)
    y = globals()['x']
    print("Global x:", y)
    globals()['x'] = 20
func()
print('Input:\n x = 10\ndef func():\n    x = 15\n    print("Local x:", x)\n    y = globals()[\'x\']\n    print("Global x:", y)\n    globals()[\'x\'] = 20\nfunc()')
print('Output:\n Modified Global x:', x)
print('-'*20)
print()
