from scripts.common import *

print('-'*30)

print("""(1) Single Underscore (_):
a) For Internal Use (_variable): If you see a variable or function starting with _, 
it's a hint that it's meant to be private and used only within the module or class where it's defined.
Example:""")

def wrapper_single_underscore_for_internal():
    class Car:
        def __init__(self):
            self._engine_type = 'V6'  # This is intended for internal use.

        def start(self):
            return f'Starting the {self._engine_type} engine.'

    my_car = Car()

    print(my_car.start())  # This is fine to use.
    print(my_car._engine_type)  # This works, but you shouldn't do this outside the class definition.

print_function(wrapper_single_underscore_for_internal)

print('-'*30)

print("""b) As a Temporary or Ignored Variable (_):
If you see _ by itself, it's often used to indicate that you don't plan to use this variable.
Example:""")

def wrapper_single_underscore_for_ignore():
    for _ in range(5):
        print("Hello!")  # The loop counter isn't needed, so it's just `_`.

print_function(wrapper_single_underscore_for_ignore)

print('-'*30)

print("""(2) Double Underscore (__):
a) To Avoid Conflicts in Subclasses (__variable): 
When you define a variable with two leading underscores in a class, Python changes the name to include the class name. 
This is done to keep the variable unique to that class, and if another class of the same name is defined, 
Python will keep them separate.
Example:""")

def wrapper_double_underscore_for_avoiding_conflicts():
    class Vehicle:
        def __init__(self, identification):
            self.__identification = identification  # Name mangling to keep it unique to 'Vehicle'

        def get_identification(self):
            return self.__identification  # Proper way to access the mangled name

    class Car(Vehicle):
        def __init__(self, identification, car_model):
            super().__init__(identification)  # Calling the parent class initializer
            self.car_model = car_model  # Public attribute for the car model
            self.__identification = 'CAR' + identification  # Attempt to override will not affect the 'Vehicle' attribute

        def get_car_identification(self):
            return self.__identification  # This is a different attribute, unique to 'Car'

    # Creating an instance of Car
    my_car = Car('123ABC', 'Toyota Corolla')

    # Trying to access the vehicle's identification
    print(my_car.get_identification())  # This will return '123ABC' from the Vehicle class
    print(my_car.get_car_identification())  # This will return 'CAR123ABC' from the Car class

    # Direct access will result in an AttributeError
    # print(my_car.__identification)  # This would fail because '__identification' is not visible


print_function(wrapper_double_underscore_for_avoiding_conflicts)
print('-'*30)


print("""b) Special Methods (__methodname__): 
These are methods with two leading and trailing underscores. 
They're used by Python to implement special behavior. 
For example, the __init__ method is called when a new object is created.
And __str__: Provides a human-readable string representation of an object.
Example:""")

def wrapper_double_underscore_for_special_methods():
    class Book:
        def __init__(self, title):
            self.title = title

        def __str__(self):
            return f"Book titled {self.title}"

    my_book = Book("1984")
    print(my_book)  # Calls the `__str__` method to get a string representation.

print_function(wrapper_double_underscore_for_special_methods)
print('-'*30)


print(__name__)