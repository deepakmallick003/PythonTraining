print()
print("Basic Append - Question 1")
print("Append '4' to the list. Expected output: [1, 2, 3, 4]")
nums = [1, 2, 3]
nums.append(4)
print('Input:\n nums = [1, 2, 3]')
print('Code: \n nums.append(4)')
print('Output:\n', nums)
print('-'*20)
print()

print("Clear List - Question 2")
print("Clear the entire list. Expected output: []")
nums = [1, 2, 3, 4, 5]
nums.clear()
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n nums.clear()')
print('Output:\n', nums)
print('-'*20)
print()

print("Copy List - Question 3")
print("Create a copy of the list. Expected output: [1, 2, 3]")
nums = [1, 2, 3]
nums_copy = nums.copy()
print('Input:\n nums = [1, 2, 3]')
print('Code: \n nums_copy = nums.copy()')
print('Output:\n', nums_copy)
print('-'*20)
print()

print("Count Element - Question 4")
print("Count how many times '2' appears in the list. Expected output: 2")
nums = [1, 2, 3, 2, 4]
count = nums.count(2)
print('Input:\n nums = [1, 2, 3, 2, 4]')
print('Code: \n count = nums.count(2)')
print('Output:\n', count)
print('-'*20)
print()

print("Extend List - Question 5")
print("Extend the list by appending elements from the iterable. Expected output: [1, 2, 3, 4, 5, 6]")
nums = [1, 2, 3]
to_add = [4, 5, 6]
nums.extend(to_add)
print('Input:\n nums = [1, 2, 3]\n to_add = [4, 5, 6]')
print('Code: \n nums.extend(to_add)')
print('Output:\n', nums)
print('-'*20)
print()

print("Index of Element - Question 6")
print("Find the index of the first element equal to 3. Expected output: 2")
nums = [1, 2, 3, 4, 3, 5]
index = nums.index(3)
print('Input:\n nums = [1, 2, 3, 4, 3, 5]')
print('Code: \n index = nums.index(3)')
print('Output:\n', index)
print('-'*20)
print()

print("Insert Element - Question 7")
print("Insert '4' at position 2. Expected output: [1, 2, 4, 3]")
nums = [1, 2, 3]
nums.insert(2, 4)
print('Input:\n nums = [1, 2, 3]')
print('Code: \n nums.insert(2, 4)')
print('Output:\n', nums)
print('-'*20)
print()

print("Pop Element - Question 8")
print("Remove and return the last item. Expected output: 3, and nums becomes [1, 2]")
nums = [1, 2, 3]
popped = nums.pop()
print('Input:\n nums = [1, 2, 3]')
print('Code: \n popped = nums.pop()')
print('Output:\n', popped, nums)
print('-'*20)
print()

print("Remove Element - Question 9")
print("Remove the first item from the list whose value is 2. Expected output: [1, 3]")
nums = [1, 2, 3]
nums.remove(2)
print('Input:\n nums = [1, 2, 3]')
print('Code: \n nums.remove(2)')
print('Output:\n', nums)
print('-'*20)
print()

print("Reverse List - Question 10")
print("Reverse the elements of the list in place. Expected output: [3, 2, 1]")
nums = [1, 2, 3]
nums.reverse()
print('Input:\n nums = [1, 2, 3]')
print('Code: \n nums.reverse()')
print('Output:\n', nums)
print('-'*20)
print()

print("Sort List - Question 11")
print("Sort the list in ascending order. Expected output: [1, 2, 3, 4, 5]")
nums = [3, 1, 4, 2, 5]
nums.sort()
print('Input:\n nums = [3, 1, 4, 2, 5]')
print('Code: \n nums.sort()')
print('Output:\n', nums)
print('-'*20)
print()

print("Slicing - Get Part of List - Question 12")
print("Slice the list to get elements from index 1 to 3. Expected output: [2, 3, 4]")
nums = [1, 2, 3, 4, 5]
sliced = nums[1:4]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n sliced = nums[1:4]')
print('Output:\n', sliced)
print('-'*20)
print()

print("Slicing - Negative Indices - Question 13")
print("Use negative indices to get the last three elements. Expected output: [3, 4, 5]")
nums = [1, 2, 3, 4, 5]
sliced = nums[-3:]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n sliced = nums[-3:]')
print('Output:\n', sliced)
print('-'*20)
print()

print("Slicing with Steps - Question 14")
print("Print every second element of the list. Expected output: [1, 3, 5]")
nums = [1, 2, 3, 4, 5]
stepped = nums[::2]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n stepped = nums[::2]')
print('Output:\n', stepped)
print('-'*20)
print()

print("Slicing - Reverse List - Question 15")
print("Use slicing to reverse the list. Expected output: [5, 4, 3, 2, 1]")
nums = [1, 2, 3, 4, 5]
reversed_list = nums[::-1]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n reversed_list = nums[::-1]')
print('Output:\n', reversed_list)
print('-'*20)
print()

print("Delete Element - Question 16")
print("Delete the element at index 2. Expected output: [1, 2, 4, 5]")
nums = [1, 2, 3, 4, 5]
del nums[2]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n del nums[2]')
print('Output:\n', nums)
print('-'*20)
print()

print("Delete Slice of List - Question 17")
print("Delete elements from index 1 to 3. Expected output: [1, 5]")
nums = [1, 2, 3, 4, 5]
del nums[1:4]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n del nums[1:4]')
print('Output:\n', nums)
print('-'*20)
print()

print()
print("Convert to Set - Question 18")
print("Convert the list to a set to remove duplicates. Expected output: {1, 2, 3}")
nums = [1, 2, 2, 3, 3]
nums_set = set(nums)
print('Input:\n nums = [1, 2, 2, 3, 3]')
print('Code: \n nums_set = set(nums)')
print('Output:\n', nums_set)
print('-'*20)
print()

print("List Comprehension - Question 19")
print("Create a new list with each element squared. Expected output: [1, 4, 9, 16, 25]")
nums = [1, 2, 3, 4, 5]
squared = [x**2 for x in nums]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n squared = [x**2 for x in nums]')
print('Output:\n', squared)
print('-'*20)
print()

print("Zip Two Lists - Question 20")
print("Combine two lists element-wise. Expected output: [(1, 'a'), (2, 'b'), (3, 'c')]")
nums = [1, 2, 3]
chars = ['a', 'b', 'c']
zipped = list(zip(nums, chars))
print("Input:\n nums = [1, 2, 3]\n chars = ['a', 'b', 'c']")
print('Code: \n zipped = list(zip(nums, chars))')
print('Output:\n', zipped)
print('-'*20)
print()

print("Sum of Elements - Question 24")
print("Calculate the sum of all elements in the list. Expected output: 15")
nums = [1, 2, 3, 4, 5]
total = sum(nums)
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n total = sum(nums)')
print('Output:\n', total)
print('-'*20)
print()

print("Minimum Element - Question 25")
print("Find the minimum element in the list. Expected output: 1")
nums = [5, 3, 8, 1, 4]
minimum = min(nums)
print('Input:\n nums = [5, 3, 8, 1, 4]')
print('Code: \n minimum = min(nums)')
print('Output:\n', minimum)
print('-'*20)
print()

print("Maximum Element - Question 26")
print("Find the maximum element in the list. Expected output: 9")
nums = [7, 2, 5, 9, 3]
maximum = max(nums)
print('Input:\n nums = [7, 2, 5, 9, 3]')
print('Code: \n maximum = max(nums)')
print('Output:\n', maximum)
print('-'*20)
print()

print("List Length - Question 27")
print("Find the length of the list. Expected output: 6")
nums = [1, 2, 3, 4, 5, 6]
length = len(nums)
print('Input:\n nums = [1, 2, 3, 4, 5, 6]')
print('Code: \n length = len(nums)')
print('Output:\n', length)
print('-'*20)
print()

print("Check if Element Exists - Question 28")
print("Check if '4' is in the list. Expected output: True")
nums = [1, 2, 3, 4, 5]
exists = 4 in nums
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n exists = 4 in nums')
print('Output:\n', exists)
print('-'*20)
print()

print("Convert List to String - Question 29")
print("Convert the list of characters to a string. Expected output: 'Python'")
chars = ['P', 'y', 't', 'h', 'o', 'n']
string = ''.join(chars)
print("Input:\n chars = ['P', 'y', 't', 'h', 'o', 'n']")
print("Code: \n string = ''.join(chars)")
print('Output:\n', string)
print('-'*20)
print()

print("Nested List - Access Element - Question 30")
print("Access the number '5' from the nested list. Expected output: 5")
nums = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
number = nums[1][1]
print('Input:\n nums = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]')
print('Code: \n number = nums[1][1]')
print('Output:\n', number)
print('-'*20)
print()

print("Flatten a Nested List - Question 31")
print("Flatten the nested list. Expected output: [1, 2, 3, 4, 5, 6, 7, 8, 9]")
nested_nums = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened = [num for sublist in nested_nums for num in sublist]
print('Input:\n nested_nums = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]')
print('Code: \n flattened = [num for sublist in nested_nums for num in sublist]')
print('Output:\n', flattened)
print('-'*20)
print()

print("List Multiplication - Question 32")
print("Repeat the list elements 3 times. Expected output: [1, 2, 3, 1, 2, 3, 1, 2, 3]")
nums = [1, 2, 3]
repeated = nums * 3
print('Input:\n nums = [1, 2, 3]')
print('Code: \n repeated = nums * 3')
print('Output:\n', repeated)
print('-'*20)
print()

print("List Comprehension with Condition - Question 33")
print("Create a new list with only even numbers. Expected output: [2, 4, 6]")
nums = [1, 2, 3, 4, 5, 6]
even_nums = [num for num in nums if num % 2 == 0]
print('Input:\n nums = [1, 2, 3, 4, 5, 6]')
print('Code: \n even_nums = [num for num in nums if num % 2 == 0]')
print('Output:\n', even_nums)
print('-'*20)
print()

print("Enumerate List - Question 34")
print("Enumerate the list elements. Expected output: [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')]")
nums = ['a', 'b', 'c', 'd']
enumerated = list(enumerate(nums))
print("Input:\n nums = ['a', 'b', 'c', 'd']")
print('Code: \n enumerated = list(enumerate(nums))')
print('Output:\n', enumerated)
print('-'*20)
print()

print("Convert String to List of Characters - Question 35")
print("Convert the string into a list of characters. Expected output: ['h', 'e', 'l', 'l', 'o']")
string = "hello"
chars = list(string)
print('Input:\n string = "hello"')
print("Code: \n chars = list(string)")
print('Output:\n', chars)
print('-'*20)
print()

print("List Slicing - Remove Last Element - Question 36")
print("Remove the last element using slicing. Expected output: [1, 2, 3, 4]")
nums = [1, 2, 3, 4, 5]
sliced = nums[:-1]
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n sliced = nums[:-1]')
print('Output:\n', sliced)
print('-'*20)
print()



