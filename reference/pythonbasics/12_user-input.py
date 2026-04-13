from scripts.common import *

# How to Get User Input
def input_function():
    print("\n--- How to Get User Input ---")
    print("Getting user input in Python is straightforward. You can use the input() function")
    print("to get input from the user. The input function takes a single argument, which is the")
    print("prompt message displayed to the user.")

    def example_input():
        x = input("Enter first number: ")
        y = input("Enter second number: ")
        z = x + y
        print(z)
        pass

    print_function(example_input)


# Types of Input Data
def input_data_types():
    print("\n--- Types of Input Data ---")
    print("The input() function always returns a string, regardless of what the user enters.")

    def example_input_data_types():
        x = input("Enter first number: ")
        a = int(x)
        print(a)
        pass

    print_function(example_input_data_types)


# When to Use Index Value
def using_index_value():
    print("\n--- When to Use Index Value ---")
    print("If you want to get a single character from the user, you can use the input() function and index the result.")

    def example_index_value():
        ch = input('Enter a character: ')[0]
        print(ch)
        pass

    print_function(example_index_value)


# Eval Function
def eval_function_example():
    print("\n--- Eval Function ---")
    print("The eval() function in Python is used to evaluate an expression entered by the user as a string.")

    def example_eval_function():
        x = eval(input("Enter an expression: "))
        typeOf = type(x)
        print(typeOf)
        pass

    print_function(example_eval_function)


# Passing Values from Command Line
def passing_command_line_values():
    print("\n--- Passing Values from Command Line ---")
    print("The sys module provides access to any command-line arguments via the sys.argv list.")

    def example_command_line_values():
        import sys
        x = sys.argv[1]
        y = sys.argv[2]
        z = x + y
        print(z)
        pass

    print_function(example_command_line_values)


input_function()
input_data_types()
using_index_value()
eval_function_example()
passing_command_line_values()