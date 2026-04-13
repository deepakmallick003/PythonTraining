from scripts.common import *
from array import array

# Define the question functions here    
def question_create_and_delete():
    print("\n\nQuestion:  Create an array with 5 elements and delete element with index value 2.")
    arr = array('i', [])
    for i in range(5):
        arr.append(i + 1)
    arr.pop(2)
    print_function(question_create_and_delete)
    print("Output:", arr, end="\n"+ "-"*40)

def question_reverse_array():
    print("\n\nQuestion:  Reverse an array.")
    arr = array('u', ['a', 'b', 'c', 'd'])
    for i in range(int(len(arr)/2)):
        arr[i], arr[len(arr)-i-1] = arr[len(arr)-i-1], arr[i]
    print_function(question_reverse_array)
    print("Output:", arr, end="\n"+ "-"*40)

def question_create_reverse_array():
    print("\n\nQuestion:  Create a new array with the reverse of an existing array.")
    arr = array('u', ['a', 'b', 'c', 'd'])
    arr1 = array(arr.typecode, [])
    for i in range(len(arr)):
        arr1.append(arr[len(arr)-i-1])
    print_function(question_create_reverse_array)
    print("Output:", arr, end="\n"+ "-"*401)


# Function for question 4: Append an element to the array
def question_append_element():
    print("\n\nQuestion:  Append an element to the array.")
    arr = array('i', [1, 2, 3])
    arr.append(4)
    print_function(question_append_element)
    print("Output:", arr, end="\n"+ "-"*40)

# Function for question 5: Insert an element at a specific position
def question_insert_element():
    print("\n\nQuestion:  Insert an element at a specific position.")
    arr = array('i', [1, 2, 4])
    arr.insert(2, 3)  # Insert 3 at position 2
    print_function(question_insert_element)
    print("Output:", arr, end="\n"+ "-"*40)

# Function for question 6: Remove the first occurrence of an element
def question_remove_element():
    print("\n\nQuestion:  Remove the first occurrence of an element.")
    arr = array('i', [1, 2, 3, 2, 4])
    arr.remove(2)  # Remove the first occurrence of 2
    print_function(question_remove_element)
    print("Output:", arr, end="\n"+ "-"*40)

# Function for question 7: Find the index of the first occurrence of an element
def question_find_index():
    print("\n\nQuestion:  Find the index of the first occurrence of an element.")
    arr = array('i', [1, 2, 3, 4, 5])
    index = arr.index(3)
    print_function(question_find_index)
    print("Output: Index of the first occurrence of 3 is:", index, end="\n"+ "-"*40)

# Function for question 8: Convert the array to a list
def question_convert_to_list():
    print("\n\nQuestion:  Convert the array to a list.")
    arr = array('i', [1, 2, 3, 4, 5])
    arr_list = arr.tolist()
    print_function(question_convert_to_list)
    print("Output: Array converted to list:", arr_list, end="\n"+ "-"*40)

# Function for question 9: Slice the array
def question_slice_array():
    print("\n\nQuestion:  Slice the array.")
    arr = array('i', [1, 2, 3, 4, 5])
    sliced_arr = arr[1:4]  # Slice from index 1 to 3
    print_function(question_slice_array)
    print("Output: Sliced array:", sliced_arr, end="\n"+ "-"*40)

# Function for question 10: Count occurrences of an element
def question_count_occurrences():
    print("\n\nQuestion:  Count occurrences of an element.")
    arr = array('i', [1, 2, 3, 2, 4, 2])
    count = arr.count(2)
    print_function(question_count_occurrences)
    print("Output: Number of occurrences of 2:", count, end="\n"+ "-"*40)

# Function for question 11: Extend array by appending elements from another array
def question_extend_array():
    print("\n\nQuestion:  Extend array by appending elements from another array.")
    arr1 = array('i', [1, 2, 3])
    arr2 = array('i', [4, 5, 6])
    arr1.extend(arr2)
    print_function(question_extend_array)
    print("Output: Extended array:", arr1, end="\n"+ "-"*40)

# Function for question 12: Create an array of characters
def question_create_char_array():
    print("\n\nQuestion:  Create an array of characters.")
    char_arr = array('u', ['a', 'b', 'c'])
    print_function(question_create_char_array)
    print("Output: Character array:", char_arr, end="\n"+ "-"*40)

# Function for question 13: Convert an array of bytes to a string
def question_bytes_to_string():
    print("\n\nQuestion:  Convert an array of bytes to a string.")
    byte_arr = array('b', [97, 98, 99])  # ASCII values for 'a', 'b', 'c'
    byte_str = byte_arr.tobytes().decode('utf-8')
    print_function(question_bytes_to_string)
    print("Output: String from bytes array:", byte_str, end="\n"+ "-"*40)

# Function for question 14: Create a copy of the array
def question_copy_array():
    print("\n\nQuestion:  Create a copy of the array.")
    arr = array('i', [1, 2, 3])
    arr_copy = array(arr.typecode, arr)
    print_function(question_copy_array)
    print("Output: Copy of the array:", arr_copy, end="\n"+ "-"*40)

# Function for question 15: Clear all elements from the array
def question_clear_array():
    print("\n\nQuestion:  Clear all elements from the array.")
    arr = array('i', [1, 2, 3, 4, 5])
    arr = array(arr.typecode)  # Reassign to a new empty array
    print_function(question_clear_array)
    print("Output: Array after clearing all elements:", arr, end="\n"+ "-"*40)

# Execute all the question functions
question_create_and_delete()
question_reverse_array()
question_create_reverse_array()
question_append_element()
question_insert_element()
question_remove_element()
question_find_index()
question_convert_to_list()
question_slice_array()
question_count_occurrences()
question_extend_array()
question_create_char_array()
question_bytes_to_string()
question_copy_array()
question_clear_array()
