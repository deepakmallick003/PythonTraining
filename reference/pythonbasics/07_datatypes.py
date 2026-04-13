# This Python script illustrates various built-in data types in Python.

# NoneType
print("\n--- NoneType ---")
print("Represents the absence of a value, similar to null in other languages.")
a = None
print("Example: a =", a)
print("Type of a:", type(a))

# Numbers
print("\n--- Numbers ---")
print("Can be integers, floating-point numbers, or complex numbers.")
# Integer
a = 5
print("\nInteger Example: a =", a)
print("Type of a:", type(a))
# Float
num = 2.5
print("\nFloat Example: num =", num)
print("Type of num:", type(num))
# Complex
num = 2 + 9j
print("\nComplex Example: num =", num)
print("Type of num:", type(num))

# Type Conversion
print("\n--- Type Conversion ---")
print("Converting one data type to another.")
a = 5.6
b = int(a)
k = float(b)
c = complex(4, 5)
print("Converted int:", b, "Type:", type(b))
print("Converted float:", k, "Type:", type(k))
print("Converted complex:", c, "Type:", type(c))

# Booleans
print("\n--- Booleans ---")
print("Represent True or False.")
a = True
bool_val = 3 < 5
print("Boolean Example: a =", a, "Type:", type(a))
print("Boolean Expression: 3 < 5 is", bool_val, "Type:", type(bool_val))

# Sequence Data Types
print("\n--- Sequence Data Types ---")
print("Can hold multiple values: List, Tuple, Set, String, Range.")

# List
print("\n--- List ---")
print("Ordered and mutable sequence of objects enclosed in square brackets.")
lst = [25, 36, 45, 12]
print("Example: lst =", lst)
print("Type of lst:", type(lst))

# Tuple
print("\n--- Tuple ---")
print("Ordered and immutable sequence of objects enclosed in parentheses.")
t = (25, 36, 45, 12, 7)
print("Example: t =", t)
print("Type of t:", type(t))

# Set
print("\n--- Set ---")
print("Unordered collection of unique elements enclosed in curly braces.")
s = {25, 36, 45, 12, 25, 36}
print("Example: s =", s)
print("Type of s:", type(s))

# String
print("\n--- String ---")
print("Sequence of characters enclosed in single or double quotes.")
str_val = "hello"
print("Example: str_val =", str_val)
print("Type of str_val:", type(str_val))

# Range
print("\n--- Range ---")
print("Immutable and iterable sequence of numbers.")
r = range(10)
print("Example: r =", r)
print("Type of r:", type(r))
print("List converted from range:", list(range(2, 10, 2)))

# Dictionary
print("\n--- Dictionary ---")
print("Collection of key-value pairs enclosed in curly braces.")
d = {1: 'a', 2: 'b', 3: 'c'}
print("Example: d =", d)
print("Type of d:", type(d))
d1 = {'navin': 'samsung', 'rahul': 'iphone', 'kiran': 'oneplus'}
print("Example: d1 =", d1)
print("Values of d1:", d1.values())
print("Keys of d1:", d1.keys())
print("Accessing element by key 'rahul':", d1['rahul'])
print("Using get method for key 'kiran':", d1.get('kiran'))

# Print a separator for readability
print("\n" + "-" * 50 + "\n")
