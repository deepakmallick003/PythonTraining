print("Question 1: Basic Dictionary Initialization")
print("Initialize a dictionary with string keys and integer values.")
print('Code: \n my_dict = {"Tom": 1, "Dick": 2, "Harry": 3}')
my_dict = {"Tom": 1, "Dick": 2, "Harry": 3}
print('Output:\n', my_dict)
print('-'*20)
print()

print("Question 2: Direct Access by Key")
print("Access a value by its key.")
print('Code: \n value = my_dict["Tom"]')
value = my_dict["Tom"]
print('Output:\n', value)
print('-'*20)
print()

print("Question 3: Safe Access with get()")
print("Access a value with get() to avoid KeyError.")
print('Code: \n value = my_dict.get("Tom")')
value = my_dict.get("Tom")
print('Output:\n', value)
print('Code: \n not_found = my_dict.get("Sam", "Not Found")')
not_found = my_dict.get("Sam", "Not Found")
print('Output:\n', not_found)
print('-'*20)
print()

print("Question 4: Accessing Non-Existent Key")
print("Access a non-existent key directly to demonstrate KeyError.")
print('Code: \n try:\n    value = my_dict["Sam"]\nexcept KeyError as e:\n    print(e)')
try:
    value = my_dict["Sam"]
except KeyError as e:
    print('Output:\n', e)
print('-'*20)
print()

print("Question 5: Creating Dictionary from Lists")
print("Use zip() to create a dictionary from two lists.")
keys = ["Navin", "Kiran", "Harish"]
values = ["Python", "Java", "JS"]
print('Code: \n my_dict = dict(zip(keys, values))')
my_dict = dict(zip(keys, values))
print('Output:\n', my_dict)
print('-'*20)
print()

print("Question 6: Removing a Key-Value Pair")
print("Remove a key-value pair and capture the removed value.")
print('Code: \n removed_value = my_dict.pop("Navin")')
removed_value = my_dict.pop("Navin")
print('Output:\n', removed_value)
print('Output Dict:\n', my_dict)
print('-'*20)
print()

print("Question 7: Key Existence Check")
print("Check if a key exists in the dictionary.")
print('Code: \n exists = "Kiran" in my_dict')
exists = "Kiran" in my_dict
print('Output:\n', exists)
print('-'*20)
print()

print("Question 8: All Keys in Dictionary")
print("Retrieve all keys from the dictionary.")
print('Code: \n keys = my_dict.keys()')
keys = my_dict.keys()
print('Output:\n', list(keys))
print('-'*20)
print()

print("Question 9: All Values in Dictionary")
print("Retrieve all values from the dictionary.")
print('Code: \n values = my_dict.values()')
values = my_dict.values()
print('Output:\n', list(values))
print('-'*20)
print()

print("Question 10: All Items in Dictionary")
print("Retrieve all key-value pairs from the dictionary.")
print('Code: \n items = my_dict.items()')
items = my_dict.items()
print('Output:\n', list(items))
print('-'*20)
print()

print("Question 11: Dictionary Update")
print("Update dictionary with another dictionary.")
print('Code: \n my_dict.update({"Harish": "C++"})')
my_dict.update({"Harish": "C++"})
print('Output:\n', my_dict)
print('-'*20)
print()

print("Question 12: Clear Dictionary")
print("Remove all items from the dictionary.")
print('Code: \n my_dict.clear()')
my_dict.clear()
print('Output:\n', my_dict)
print('-'*20)
print()

print("Question 13: Dictionary Copy")
print("Create a shallow copy of the dictionary.")
print('Code: \n my_dict = {"Navin": "Python"}\n new_dict = my_dict.copy()')
my_dict = {"Navin": "Python"}
new_dict = my_dict.copy()
print('Output:\n', new_dict)
print('-'*20)
print()

print("Question 14: Dictionary Comprehension")
print("Create a new dictionary with comprehension.")
print('Code: \n squares = {x: x*x for x in range(5)}')
squares = {x: x*x for x in range(5)}
print('Output:\n', squares)
print('-'*20)
print()

print("Question 15: Nested Dictionary Access")
print("Access a nested dictionary value.")
print('Code: \n my_dict = {"Navin": {"language": "Python"}}\n language = my_dict["Navin"]["language"]')
my_dict = {"Navin": {"language": "Python"}}
language = my_dict["Navin"]["language"]
print('Output:\n', language)
print('-'*20)
print()

print("Question 16: Sorting Dictionary by Keys")
print("Sort the dictionary by its keys and display the key-value pairs in sorted order.")
my_dict = {"banana": 3, "apple": 4, "pear": 1, "orange": 2}
print('Input:\n my_dict = {"banana": 3, "apple": 4, "pear": 1, "orange": 2}')
sorted_keys = sorted(my_dict.keys())
print('Code: \n sorted_keys = sorted(my_dict.keys())')
print('Output (Sorted by keys):\n', [(key, my_dict[key]) for key in sorted_keys])
print('-'*20)
print()

print("Question 17: Sorting Dictionary by Values")
print("Sort the dictionary by its values and display the key-value pairs in sorted order.")
print('Code: \n sorted_items = sorted(my_dict.items(), key=lambda item: item[1])')
sorted_items = sorted(my_dict.items(), key=lambda item: item[1])
print('Output (Sorted by values):\n', sorted_items)
print('-'*20)
print()

print("Question 18: Reversing Dictionary Order")
print("Reverse the order of key-value pairs in the dictionary.")
print('Input:\n my_dict = {"one": 1, "two": 2, "three": 3}')
my_dict = {"one": 1, "two": 2, "three": 3}
print('Code: \n reversed_items = list(my_dict.items())[::-1]')
reversed_items = list(my_dict.items())[::-1]
print('Output (Reversed order):\n', reversed_items)
print('-'*20)
print()

print("Question 19: Creating Dictionary from Two Lists with zip")
print("Create a dictionary by combining two lists using the zip function.")
keys = ["one", "two", "three"]
values = [1, 2, 3]
print('Input:\n keys = ["one", "two", "three"]\n values = [1, 2, 3]')
print('Code: \n combined_dict = dict(zip(keys, values))')
combined_dict = dict(zip(keys, values))
print('Output:\n', combined_dict)
print('-'*20)
print()

print("Question 20: Extracting Lists from a Dictionary")
print("Extract separate lists of keys and values from a dictionary.")
print('Code: \n keys_list, values_list = zip(*combined_dict.items())')
keys_list, values_list = zip(*combined_dict.items())
print('Output (Keys list):\n', list(keys_list))
print('Output (Values list):\n', list(values_list))
print('-'*20)
print()
