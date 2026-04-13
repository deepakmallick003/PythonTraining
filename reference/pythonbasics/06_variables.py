# This Python script illustrates various key concepts related to variables in Python.

# Concept 1: Variables and Memory
print("\nConcept 1: Variables and Memory")
print("- Every variable in Python has its own address.")
print("- The id() function returns the 'identity' of an object, which is unique and constant for this object during its lifetime.")

# Example for id() function
x = 10
print("x =", x)
print("Address of x:", id(x))

# Assigning value of one variable to another
y = x
print("\ny = x")
print("Address of y:", id(y))

# Changing value of a variable
x = 15
print("\nx = 15")
print("New value of x:", x)
print("Address of x after change:", id(x))
print("Value of y remains unchanged:", y)
print("Address of y remains unchanged:", id(y))

# Concept 2: Garbage Collection
print("\nConcept 2: Garbage Collection")
print("- Python automatically removes data that is not referenced by any variable from memory.")

# Example for Garbage Collection
z = 20
print("\nz = 20")
print("Address of z before reassignment:", id(z))
z = 25  # The old value 20 is now unreferenced and subject to garbage collection
print("\nz = 25")
print("Address of z after reassignment:", id(z))

# Concept 3: Constants and Types
print("\nConcept 3: Constants and Types")
print("- The value of variables can change, but constants should remain unchanged.")
print("- Constants are represented by all capital letters by convention.")
print("- The type() function returns the data type of the value of a variable.")

# Example for Constants and type() function
PI = 3.14159
print("\nPI =", PI)
print("Type of PI:", type(PI))

# Example for Custom Types (Creating a simple class)
class Car:
    def __init__(self, brand):
        self.brand = brand

my_car = Car("Toyota")
print("\nmy_car = Car('Toyota')")
print("Type of my_car:", type(my_car))

# Additional Information on Python Variables
print("\nAdditional Information on Python Variables")
print("- In Python, variables are references to objects in memory, similar to pointers in C.")
print("- The distinction between 'value types' and 'reference types' is not applicable in Python; all variables are references to objects.")

# Example to illustrate reference behavior
list1 = [1, 2, 3]
list2 = list1
print("\nlist1 =", list1)
print("list2 = list1")
list1.append(4)
print("After appending to list1, list2 reflects the change:", list2)
print("Address of list1:", id(list1))
print("Address of list2:", id(list2), " (same as list1)")

# Print a separator for readability
print("\n" + "-" * 50 + "\n")