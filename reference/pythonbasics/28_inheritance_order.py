'''
During inheritance, the constructor (__init__) of the parent class is not automatically called;
it must be called explicitly if the child class defines its own constructor.

MRO is the order in which Python looks for a method in a hierarchy of classes.

It follows the depth-first, left-to-right rule.

__init__ method resolution follows MRO; the first __init__ found in the MRO chain will be executed.
'''

class A:
    def __init__(self):
        print("A __init__")

class B(A):
    def __init__(self):
        print("B __init__")
        super().__init__()

class C(A):
    def __init__(self):
        print("C __init__")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D __init__")
        super().__init__()

# Usage
d = D()
# Output:
# D __init__
# B __init__
# C __init__
# A __init__
