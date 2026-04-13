print()
print("Squaring Numbers - Question 1")
print("Square each element of the list [1, 2, 3]. Expected output: [1, 4, 9]")
square = lambda x: x**2
squared = list(map(square, [1, 2, 3]))
print('Input:\n squared = list(map(lambda x: x**2, [1, 2, 3]))')
print('Code: \n squared = list(map(lambda x: x**2, [1, 2, 3]))')
print('Output:\n', squared)
print('-'*20)
print()

print("Adding Numbers - Question 2")
print("Add 3 and 4 using a lambda function. Expected output: 7")
add = lambda x, y: x + y
result = add(3, 4)
print('Input:\n add = lambda x, y: x + y\n result = add(3, 4)')
print('Code: \n add = lambda x, y: x + y\n result = add(3, 4)')
print('Output:\n', result)
print('-'*20)
print()

print("Sorting Tuples - Question 3")
print("Sort the list of tuples [(2, 'b'), (1, 'a')] by the second element. Expected output: [(1, 'a'), (2, 'b')]")
sorted_tuples = sorted([(2, 'b'), (1, 'a')], key=lambda x: x[1])
print('Input:\n sorted_tuples = sorted([(2, \'b\'), (1, \'a\')], key=lambda x: x[1])')
print('Code: \n sorted_tuples = sorted([(2, \'b\'), (1, \'a\')], key=lambda x: x[1])')
print('Output:\n', sorted_tuples)
print('-'*20)
print()

print()
print("Filtering Even Numbers - Question 4")
print("Filter out the even numbers from the list [3, 2, 6, 8, 4, 6, 2, 9]. Expected output: [2, 6, 8, 4, 6, 2]")
nums = [3, 2, 6, 8, 4, 6, 2, 9]
iseven = lambda n: n % 2 == 0
evens = list(filter(iseven, nums))
print('Input:\n nums = [3, 2, 6, 8, 4, 6, 2, 9]\n evens = list(filter(lambda n: n % 2 == 0, nums))')
print('Code: \n evens = list(filter(lambda n: n % 2 == 0, nums))')
print('Output:\n', evens)
print('-'*20)
print()


print()
print("Summation with Reduce - Question 5")
print("Use the reduce function to compute the sum of the list [1, 2, 3, 4, 5]. Expected output: 15")
from functools import reduce
nums = [1, 2, 3, 4, 5]
sum_of_nums = reduce(lambda a, b: a + b, nums)
print('Input:\n nums = [1, 2, 3, 4, 5]')
print('Code: \n sum_of_nums = reduce(lambda a, b: a + b, nums)')
print('Output:\n', sum_of_nums)
print('-'*20)
print()

print()
print("Maximum with Reduce - Question 6")
print("Use the reduce function to find the maximum number in the list [47, 11, 42, 102, 13]. Expected output: 102")
from functools import reduce
nums = [47, 11, 42, 102, 13]
max_num = reduce(lambda a, b: a if a > b else b, nums)
print('Input:\n nums = [47, 11, 42, 102, 13]')
print('Code: \n max_num = reduce(lambda a, b: a if a > b else b, nums)')
print('Output:\n', max_num)
print('-'*20)
print()

