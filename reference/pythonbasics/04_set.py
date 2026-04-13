print("Create Set - Question 1")
print("Create a set with elements {1, 2, 3}. Expected output: {1, 2, 3}")
print('Input:\n None')
print('Code: \n set1 = {1, 2, 3}')
set1 = {1, 2, 3}
print('Output:\n', set1)
print('-'*20)
print()

print("Add Element - Question 2")
print("Add element '4' to the set. Expected output: {1, 2, 3, 4}")
set1 = {1, 2, 3}
print('Input:\n set1 = {1, 2, 3}')
print('Code: \n set1.add(4)')
set1.add(4)
print('Output:\n', set1)
print('-'*20)
print()

print("Remove Element - Question 3")
print("Remove element '2' from the set. Expected output: {1, 3, 4}")
set1 = {1, 2, 3, 4}
print('Input:\n set1 = {1, 2, 3, 4}')
print('Code: \n set1.remove(2)')
set1.remove(2)
print('Output:\n', set1)
print('-'*20)
print()

print("Set Union - Question 4")
print("Union of two sets {1, 2, 3} and {3, 4, 5}. Expected output: {1, 2, 3, 4, 5}")
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print('Input:\n set1 = {1, 2, 3}\n set2 = {3, 4, 5}')
print('Code: \n union_set = set1.union(set2)')
union_set = set1.union(set2)
print('Output:\n', union_set)
print('-'*20)
print()

print("Set Intersection - Question 5")
print("Intersection of two sets {1, 2, 3} and {2, 3, 4}. Expected output: {2, 3}")
set1 = {1, 2, 3}
set2 = {2, 3, 4}
print('Input:\n set1 = {1, 2, 3}\n set2 = {2, 3, 4}')
print('Code: \n intersection_set = set1.intersection(set2)')
intersection_set = set1.intersection(set2)
print('Output:\n', intersection_set)
print('-'*20)
print()

print("Set Difference - Question 6")
print("Difference of two sets {1, 2, 3} and {2, 3, 4}. Expected output: {1}")
set1 = {1, 2, 3}
set2 = {2, 3, 4}
print('Input:\n set1 = {1, 2, 3}\n set2 = {2, 3, 4}')
print('Code: \n difference_set = set1.difference(set2)')
difference_set = set1.difference(set2)
print('Output:\n', difference_set)
print('-'*20)
print()

print("Set Symmetric Difference - Question 7")
print("Symmetric difference of two sets {1, 2, 3} and {3, 4, 5}. Expected output: {1, 2, 4, 5}")
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print('Input:\n set1 = {1, 2, 3}\n set2 = {3, 4, 5}')
print('Code: \n sym_diff_set = set1.symmetric_difference(set2)')
sym_diff_set = set1.symmetric_difference(set2)
print('Output:\n', sym_diff_set)
print('-'*20)
print()

print("Check Subset - Question 8")
print("Check if {1, 2} is a subset of {1, 2, 3}. Expected output: True")
set1 = {1, 2}
set2 = {1, 2, 3}
print('Input:\n set1 = {1, 2}\n set2 = {1, 2, 3}')
print('Code: \n is_subset = set1.issubset(set2)')
is_subset = set1.issubset(set2)
print('Output:\n', is_subset)
print('-'*20)
print()

print("Check Superset - Question 9")
print("Check if {1, 2, 3} is a superset of {1, 2}. Expected output: True")
set1 = {1, 2, 3}
set2 = {1, 2}
print('Input:\n set1 = {1, 2, 3}\n set2 = {1, 2}')
print('Code: \n is_superset = set1.issuperset(set2)')
is_superset = set1.issuperset(set2)
print('Output:\n', is_superset)
print('-'*20)
print()

print("Convert List to Set - Question 10")
print("Convert list [1, 2, 2, 3, 3] to a set to remove duplicates. Expected output: {1, 2, 3}")
list1 = [1, 2, 2, 3, 3]
print('Input:\n list1 = [1, 2, 2, 3, 3]')
print('Code: \n set_from_list = set(list1)')
set_from_list = set(list1)
print('Output:\n', set_from_list)
print('-'*20)
print()

print("Set vs List - Efficiency in Membership Testing - Question 11")
print("Compare the time taken to check the membership of an element in a large set and a large list.")
import time
import random
# Create a large set and list
large_set = set(range(1000000))
large_list = list(range(1000000))
search_element = random.randint(0, 1000000)
print('Input:\n A large set and list with 1 million elements each')
# Measure time for membership testing in the set
start_time = time.time()
is_member_set = search_element in large_set
set_time = time.time() - start_time
print('Code: \n is_member_set = search_element in large_set')
print('Set Membership Test Time:\n {:.6f} seconds'.format(set_time))
# Measure time for membership testing in the list
start_time = time.time()
is_member_list = search_element in large_list
list_time = time.time() - start_time
print('Code: \n is_member_list = search_element in large_list')
print('List Membership Test Time:\n {:.6f} seconds'.format(list_time))
print('-'*20)
print()

print("Set vs List - Unordered Nature of Sets - Question 12")
print("Illustrate that sets do not maintain the order of elements.")
# Create a list and convert it to a set
initial_list = [11, 4, 42, 23]
converted_set = set(initial_list)
print('Input:\n initial_list = [11, 4, 42, 23]')
# Display the list and the set
print('Code: \n converted_set = set(initial_list)')
print('Initial List:\n', initial_list)
print('Converted Set:\n', converted_set)
print("NOTE: When a set is initialized, Python uses a hash table to store its elements. Each element's hash value determines its position in the hash table")
print("The order of elements in a set is based on their hash values, not the order in which they are added. This results in the set being unordered.")
print("The observed order of elements in a set ({42, 11, 4, 23}) is consistent due to the specific hash function implementation in Python for integers.")
print("But this consistency is not guaranteed and should not be relied upon.")
print('-'*20)
print()
