print("Create Tuple - Question 1")
print("Create a tuple with elements (1, 2, 3). Expected output: (1, 2, 3)")
print('Input:\n None')
print('Code: \n tuple1 = (1, 2, 3)')
tuple1 = (1, 2, 3)
print('Output:\n', tuple1)
print('-'*20)
print()

print("Count Element - Question 2")
print("Count how many times '3' appears in the tuple. Expected output: 1")
tuple1 = (1, 2, 3, 4, 3)
print('Input:\n tuple1 = (1, 2, 3, 4, 3)')
print('Code: \n count = tuple1.count(3)')
count = tuple1.count(3)
print('Output:\n', count)
print('-'*20)
print()

print("Index of Element - Question 3")
print("Find the index of the first element equal to 3. Expected output: 2")
tuple1 = (1, 2, 3, 4, 3)
print('Input:\n tuple1 = (1, 2, 3, 4, 3)')
print('Code: \n index = tuple1.index(3)')
index = tuple1.index(3)
print('Output:\n', index)
print('-'*20)
print()

print("Unpacking Tuple - Question 4")
print("Unpack the tuple into three variables a, b, c. Expected output: a=1, b=2, c=3")
tuple1 = (1, 2, 3)
print('Input:\n tuple1 = (1, 2, 3)')
print('Code: \n a, b, c = tuple1')
a, b, c = tuple1
print('Output:\n a={}, b={}, c={}'.format(a, b, c))
print('-'*20)
print()

print("Concatenate Tuples - Question 5")
print("Concatenate two tuples. Expected output: (1, 2, 3, 4, 5)")
tuple1 = (1, 2, 3)
tuple2 = (4, 5)
print('Input:\n tuple1 = (1, 2, 3)\n tuple2 = (4, 5)')
print('Code: \n tuple3 = tuple1 + tuple2')
tuple3 = tuple1 + tuple2
print('Output:\n', tuple3)
print('-'*20)
print()

print("Check Element in Tuple - Question 6")
print("Check if '4' is in the tuple. Expected output: True")
tuple1 = (1, 2, 3, 4, 5)
print('Input:\n tuple1 = (1, 2, 3, 4, 5)')
print('Code: \n exists = 4 in tuple1')
exists = 4 in tuple1
print('Output:\n', exists)
print('-'*20)
print()

print("Tuple Length - Question 7")
print("Find the length of the tuple. Expected output: 5")
tuple1 = (1, 2, 3, 4, 5)
print('Input:\n tuple1 = (1, 2, 3, 4, 5)')
print('Code: \n length = len(tuple1)')
length = len(tuple1)
print('Output:\n', length)
print('-'*20)
print()

print("Nested Tuple Access - Question 8")
print("Access the element 'b' from the nested tuple. Expected output: 'b'")
tuple1 = (1, ('a', 'b', 'c'), 3)
print('Input:\n tuple1 = (1, (\'a\', \'b\', \'c\'), 3)')
print('Code: \n element = tuple1[1][1]')
element = tuple1[1][1]
print('Output:\n', element)
print('-'*20)
print()

print("Tuple to List Conversion - Question 9")
print("Convert the tuple to a list. Expected output: [1, 2, 3, 4, 5]")
tuple1 = (1, 2, 3, 4, 5)
print('Input:\n tuple1 = (1, 2, 3, 4, 5)')
print('Code: \n list1 = list(tuple1)')
list1 = list(tuple1)
print('Output:\n', list1)
print('-'*20)
print()

print("Immutable Nature of Tuples - Question 10")
print("Attempt to change the first element of the tuple to 100. Expected output: TypeError")
tuple1 = (1, 2, 3)
print('Input:\n tuple1 = (1, 2, 3)')
try:
    tuple1[0] = 100
except TypeError as e:
    print('Code: \n tuple1[0] = 100')
    print('Output:\n', e)
print('-'*20)
print()

print("Tuple Repetition - Question 11")
print("Repeat the elements of the tuple three times. Expected output: (1, 2, 3, 1, 2, 3, 1, 2, 3)")
tuple1 = (1, 2, 3)
print('Input:\n tuple1 = (1, 2, 3)')
print('Code: \n repeated_tuple = tuple1 * 3')
repeated_tuple = tuple1 * 3
print('Output:\n', repeated_tuple)
print('-'*20)
print()

print("Minimum and Maximum - Question 12")
print("Find the minimum and maximum values in the tuple. Expected output: Min: 1, Max: 5")
tuple1 = (2, 3, 5, 1, 4)
print('Input:\n tuple1 = (2, 3, 5, 1, 4)')
min_val = min(tuple1)
max_val = max(tuple1)
print('Code: \n min_val = min(tuple1)\n max_val = max(tuple1)')
print('Output: Min:', min_val, ', Max:', max_val)
print('-'*20)
print()

print("Tuple and List Conversion - Question 13")
print("Convert a list to a tuple and vice versa. Expected output: Tuple: (1, 2, 3), List: [1, 2, 3]")
list1 = [1, 2, 3]
print('Input:\n list1 = [1, 2, 3]')
tuple_converted = tuple(list1)
list_converted = list(tuple_converted)
print('Code: \n tuple_converted = tuple(list1)\n list_converted = list(tuple_converted)')
print('Output: Tuple:', tuple_converted, ', List:', list_converted)
print('-'*20)
print()

print("Tuple Slicing - Question 14")
print("Slice the tuple to get the first three elements. Expected output: (1, 2, 3)")
tuple1 = (1, 2, 3, 4, 5)
print('Input:\n tuple1 = (1, 2, 3, 4, 5)')
print('Code: \n sliced_tuple = tuple1[:3]')
sliced_tuple = tuple1[:3]
print('Output:\n', sliced_tuple)
print('-'*20)
print()

print("Nested Tuples - Question 15")
print("Create a nested tuple and access the second element of the first tuple. Expected output: 'b'")
nested_tuple = (('a', 'b'), ('c', 'd'))
print('Input:\n nested_tuple = ((\'a\', \'b\'), (\'c\', \'d\'))')
print('Code: \n element = nested_tuple[0][1]')
element = nested_tuple[0][1]
print('Output:\n', element)
print('-'*20)
print()


print("List vs Tuple - Performance Comparison - Question 16")
print("Measure the time taken to access all elements in a large list and a large tuple. Expected outcome: Faster access in tuple.")
import time
# Create a large list and tuple with the same elements
large_list = list(range(1000000))  # A list with 1 million elements
large_tuple = tuple(range(1000000))  # A tuple with the same elements
# Function to iterate over a collection and access each element
def access_elements(collection):
    for element in collection:
        _ = element  # Access and do nothing
print('Input:\n Create a large list and tuple with 1 million elements each')
# Measure performance for the list
start_time = time.time()
access_elements(large_list)
list_time = time.time() - start_time
print('Code: \n Access each element in the large list')
print('List Access Time:\n {:.6f} seconds'.format(list_time))
# Measure performance for the tuple
start_time = time.time()
access_elements(large_tuple)
tuple_time = time.time() - start_time
print('Code: \n Access each element in the large tuple')
print('Tuple Access Time:\n {:.6f} seconds'.format(tuple_time))
print('-'*20)
print()


print("List vs Tuple - Data Integrity and Mutability- Question 17")
print("Compare the use of a list for mutable data and a tuple for immutable data.")
# Scenario 1: Mutable Data (List)
print("\n--- Scenario 1: Mutable Data (List) ---")
print("Manage an inventory of items where quantities change over time.")
inventory = ["apples", "oranges", "bananas"]
print('Input:\n inventory = ["apples", "oranges", "bananas"]')
# Function to update inventory
def add_item_to_inventory(inventory, item):
    inventory.append(item)
# Add an item and display updated inventory
add_item_to_inventory(inventory, "grapes")
print('Code: \n add_item_to_inventory(inventory, "grapes")')
print('Updated Inventory:\n', inventory)
# Scenario 2: Immutable Data (Tuple)
print("\n--- Scenario 2: Immutable Data (Tuple) ---")
print("Store fixed geographical coordinates that should not change.")
coordinates = (40.7128, -74.0060)
print('Input:\n coordinates = (40.7128, -74.0060)')
# Function to display coordinates
def display_coordinates(coords):
    print('Coordinates:\n Latitude:', coords[0], '\n Longitude:', coords[1])
# Display coordinates
print('Code: \n display_coordinates(coordinates)')
display_coordinates(coordinates)
# Attempt to change the tuple (illustrating immutability)
try:
    coordinates[0] = 41.0000
except TypeError as e:
    print('\nAttempt to modify tuple data:\n', e)
print('-'*20)
print()


