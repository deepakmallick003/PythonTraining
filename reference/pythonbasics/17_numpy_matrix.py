from numpy import *

# Question Set on Arrays and Matrices

# 1-D Array Creation and Properties
print("1-D Array Creation - Question 1")
print("Create a 1-D array with elements [1, 2, 3], and display its dtype and ndim. Expected output: dtype: int32, ndim: 1")
arr = array([1, 2, 3])
print('Input:\n arr = array([1, 2, 3])')
print('Code: \n print(arr.dtype)\n print(arr.ndim)')
print('Output:\n', arr.dtype, '\n', arr.ndim)
print('-'*20)
print()

# 2-D Array Creation and Properties
print("2-D Array Creation - Question 2")
print("Create a 2-D array with elements [[1, 2], [3, 4]], and display its shape and size. Expected output: shape: (2, 2), size: 4")
arr2d = array([[1, 2], [3, 4]])
print('Input:\n arr2d = array([[1, 2], [3, 4]])')
print('Code: \n print(arr2d.shape)\n print(arr2d.size)')
print('Output:\n', arr2d.shape, '\n', arr2d.size)
print('-'*20)
print()

# Reshape 1-D to 2-D Array
print("Array Reshaping 1-D to 2-D - Question 3")
print("Reshape the 1-D array [1, 2, 3, 4] to a 2-D array of shape (2, 2). Expected output: [[1 2] [3 4]]")
arr_reshape = array([1, 2, 3, 4]).reshape(2, 2)
print('Input:\n array([1, 2, 3, 4]).reshape(2, 2)')
print('Code: \n arr_reshape = array([1, 2, 3, 4]).reshape(2, 2)')
print('Output:\n', arr_reshape)
print('-'*20)
print()

# Reshape 1-D to 3-D Array
print("Array Reshaping 1-D to 3-D - Question 4")
print("Reshape the 1-D array [1, 2, 3, 4, 5, 6, 7, 8] to a 3-D array of shape (2, 2, 2). Expected output: [[[1 2] [3 4]] [[5 6] [7 8]]]")
arr3d = array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(2, 2, 2)
print('Input:\n array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(2, 2, 2)')
print('Code: \n arr3d = array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(2, 2, 2)')
print('Output:\n', arr3d)
print('-'*20)
print()

# Matrix Creation from Array
print("Matrix Creation from Array - Question 5")
print("Convert the 2-D array [[1, 2], [3, 4]] to a matrix. Expected output: matrix([[1, 2], [3, 4]])")
matrix_from_arr = matrix([[1, 2], [3, 4]])
print('Input:\n matrix([[1, 2], [3, 4]])')
print('Code: \n matrix_from_arr = matrix([[1, 2], [3, 4]])')
print('Output:\n', matrix_from_arr)
print('-'*20)
print()

# Matrix Diagonal Elements
print("Matrix Diagonal - Question 6")
print("Print the diagonal elements of the matrix [[1, 2], [3, 4]]. Expected output: [1 4]")
matrix_diag = matrix('1 2; 3 4')
print('Input:\n matrix(\'1 2; 3 4\')')
print('Code: \n matrix_diag.diagonal()')
print('Output:\n', matrix_diag.diagonal())
print('-'*20)
print()


print()
print("Direct Matrix Creation - Question 7")
print("Create a matrix directly using the 'matrix()' attribute with the input '1 2 3 6 ; 4 5 6 7'. Expected output: matrix([[1, 2, 3, 6], [4, 5, 6, 7]])")
mat = matrix('1 2 3 6 ; 4 5 6 7')
print('Input:\n matrix(\'1 2 3 6 ; 4 5 6 7\')')
print('Code: \n mat = matrix(\'1 2 3 6 ; 4 5 6 7\')')
print('Output:\n', mat)
print('-'*20)
print()
