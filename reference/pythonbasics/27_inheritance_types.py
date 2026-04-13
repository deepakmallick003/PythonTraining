##Single

class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

# Usage
buddy = Dog()
buddy.speak()  # Output: Animal speaks
buddy.bark()   # Output: Dog barks



##Multilevel
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

class Puppy(Dog):
    def weep(self):
        print("Puppy weeps")

# Usage
tiny = Puppy()
tiny.speak()  # Output: Animal speaks
tiny.bark()   # Output: Dog barks
tiny.weep()   # Output: Puppy weeps



### Multiple
class Father:
    def height(self):
        print("Height from father")

class Mother:
    def intelligence(self):
        print("Intelligence from mother")

class Child(Father, Mother):
    pass

# Usage
child = Child()
child.height()        # Output: Height from father
child.intelligence()  # Output: Intelligence from mother

