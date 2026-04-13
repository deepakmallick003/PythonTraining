"""
Duck typing is a concept in programming where the focus is on what an object can do, rather than what it is.
The name Duck Typing comes from the phrase:
“If it looks like a duck and quacks like a duck, it’s a duck”

Why Duck Typing is Needed?
Duck typing enhances flexibility and allows for more generic programming.
It enables functions or methods to accept any object that has the required set of methods or attributes,
leading to code that is easier to maintain and extend.

Justified Scenario with Code:
Imagine a function that needs to save data.
It doesn't need to know if it's writing to a file, a network socket, or just printing to the console;
it only needs a "save" method.
"""

class FileSaver:
    def save(self, data):
        with open('data.txt', 'w') as file:
            file.write(data)

class ConsoleSaver:
    def save(self, data):
        print(data)

def store_data(saver, data):
    saver.save(data)

file_saver = FileSaver()
console_saver = ConsoleSaver()

store_data(file_saver, 'Data to save')  # Saves to a file
store_data(console_saver, 'Data to save')  # Prints to the console




"""
Key Points with Code Examples:
"""

"""
1) Behavior Over Type:
Example: go_skyhigh function, accepts any object with a fly method.
"""

"""
2) Flexibility:
Example: compose function, can use any object with a write method to compose text.
"""
class Pen:
    def write(self):
        print("Writing with a pen.")

class Keyboard:
    def write(self):
        print("Typing with a keyboard.")

def compose(writer):
    writer.write()

pen = Pen()
keyboard = Keyboard()

compose(pen)       # Output: Writing with a pen.
compose(keyboard)  # Output: Typing with a keyboard.



"""
3) Runtime Type Checking:
Example: pet_speak function, uses hasattr to check for a bark method at runtime.
"""
class Dog:
    def bark(self):
        print("Woof!")

def pet_speak(pet):
    if hasattr(pet, 'bark'):
        pet.bark()
    else:
        print("This pet doesn't bark.")

dog = Dog()
pet_speak(dog)  # Output: Woof!
pet_speak("I'm not a pet")  # Output: This pet doesn't bark.


"""
4) Error Potential:
Example: start_trip function, will raise an error if the object doesn't have a drive method.
"""
class Car:
    def drive(self):
        print("Car is driving.")

def start_trip(vehicle):
    vehicle.drive()  # Assuming that the vehicle can drive.

car = Car()
start_trip(car)  # Works fine.

bicycle = "I'm a bicycle"
start_trip(bicycle)  # AttributeError: 'str' object has no attribute 'drive'


"""
5) hasattr() and getattr():
Example: perform_operation function, checks and calls a method by name on an object using hasattr and getattr.
"""

class Calculator:
    def calculate(self):
        return "Calculating result."

def perform_operation(machine, operation):
    if hasattr(machine, operation):
        func = getattr(machine, operation)
        print(func())
    else:
        print(f"Operation {operation} not supported.")

calc = Calculator()
perform_operation(calc, 'calculate')  # Output: Calculating result.
perform_operation(calc, 'print')      # Output: Operation print not supported.
