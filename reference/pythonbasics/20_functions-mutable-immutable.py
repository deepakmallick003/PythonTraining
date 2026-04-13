from scripts.common import *

def behavior_expectation():
    print("\n--- Behavior Expectation ---")
    print(
        "Description: Immutable objects can't be modified, so functions can't change them. Mutable objects can be changed, so functions can alter them.")

    # Immutable Example
    def append_suffix(name):
        return name + "_suffix"

    print("\nFunction: append_suffix")
    print_function(append_suffix)
    original_name = "deepak"
    print("Input: original_name =", original_name)
    modified_name = append_suffix(original_name)
    print("Output: modified_name =", modified_name)

    # Mutable Example
    def add_item_to_list(lst):
        lst.append("new item")
        return lst

    print("\nFunction: add_item_to_list")
    print_function(add_item_to_list)
    my_list = ["item1", "item2"]
    print("Input: my_list =", my_list)
    modified_list = add_item_to_list(my_list.copy())
    print("Output: modified_list =", modified_list)


def function_side_effects():
    print("\n--- Function Side-Effects ---")
    print("Description: Functions can have side effects on mutable objects, changing their state.")

    def modify_list(lst):
        lst.append("modified")
        return lst

    print("\nFunction: modify_list")
    print_function(modify_list)
    my_list = ["original"]
    print("Input: my_list =", my_list)
    new_list = modify_list(my_list)
    print("Output: new_list =", new_list)
    print("Original list after modification:", my_list)


def copying_behavior():
    print("\n--- Copying Behavior ---")
    print("Description: Shallow copying of mutable objects allows independent modifications of the copy and original.")

    original_list = [1, 2, 3]
    copied_list = original_list.copy()
    copied_list.append(4)
    print("\nOriginal List:", original_list)
    print("Copied List:", copied_list)


def design_intent():
    print("\n--- Design Intent ---")
    print("Description: Using immutable objects signals that the data should not be modified.")

    coordinates = (10.0, 20.0)
    print("\nImmutable Tuple (Coordinates):", coordinates)


def optimization_memory_usage():
    print("\n--- Optimization and Memory Usage ---")
    print("Description: Python optimizes the usage of immutable objects.")

    a = 10
    b = 10
    print("\nInteger Caching Example: 'a' is 'b':", a is b)


def functional_programming_style():
    print("\n--- Functional Programming Style ---")
    print("Description: Immutable data types are conducive to a functional programming style.")

    def sum_values(values):
        return sum(values)

    print("\nFunction: sum_values")
    print_function(sum_values)
    numbers = (1, 2, 3)
    print("Input: numbers =", numbers)
    result = sum_values(numbers)
    print("Output: Sum =", result)


def data_type_behaviors_on_change():
    print("\n--- Data Type Behaviors on Change ---")
    print("Description: This function demonstrates how different data types behave when they are modified.")

    # Function to modify an integer
    def change_int(n):
        n += 10
        print("Integer value in function after modification:", n)
        return n

    # Function to modify a string
    def change_str(s):
        s = 'deepak mallick'
        print("String value in function after modification:", s)
        return s

    # Function to modify a list
    def change_list(lst):
        lst[0]=0
        print("List value in function after modification:", lst)
        return lst

    # Function to reassign a tuple
    def reassign_tuple(t):
        t = (4,5,6)
        print("Tuple value in function after reassignment:", t)
        return t

    # Function to modify a set
    def change_set(st):
        st.add(7)
        print("Set value in function after modification:", st)
        return st

    # Function to reassign a set
    def reassign_set(st):
        st = {4,5,6}
        print("Set value in function after reassignment:", st)
        return st

    # Integer
    n = 5
    print("\nOriginal integer:", n)
    print("\nFunction:")
    print_function(change_int)
    change_int(n)
    print("Original Integer value:", n)

    # String
    s = 'deepak'
    print("\nOriginal string:", s)
    print("\nFunction:")
    print_function(change_str)
    change_str(s)
    print("Original String value:", s)

    # List
    lst = [1, 2, 3]
    print("\nOriginal list:", lst)
    print("\nFunction:")
    print_function(change_list)
    change_list(lst)
    print("Original List value:", lst)

    # Tuple
    t = (1, 2, 3)
    print("\nOriginal tuple:", t)
    print("\nFunction:")
    print_function(reassign_tuple)
    reassign_tuple(t)
    print("Original Tuple value:", t)

    # Set Change
    st = {1, 2, 3}
    print("\nOriginal set:", st)
    print("\nFunction:")
    print_function(change_set)
    change_set(st)
    print("Original Set value:", st)

    # Set Reassign
    st = {1, 2, 3}
    print("\nOriginal set:", st)
    print("\nFunction:")
    print_function(reassign_set)
    reassign_set(st)
    print("Original Set value:", st)

# Main section to execute and display each concept
behavior_expectation()
function_side_effects()
copying_behavior()
design_intent()
optimization_memory_usage()
functional_programming_style()
data_type_behaviors_on_change()
