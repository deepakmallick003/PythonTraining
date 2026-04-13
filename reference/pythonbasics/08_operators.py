# Creating a Python file content with detailed explanations and code examples for different types of operators

# This Python script illustrates various operators in Python along with their descriptions and examples.

# Arithmetic Operators
print("\n--- Arithmetic Operators ---")
print("Operator: + (Addition)\nDescription: Adds two operands\nExample: 5 + 3 =", 5 + 3)
print("\nOperator: - (Subtraction)\nDescription: Subtracts the second operand from the first\nExample: 5 - 3 =", 5 - 3)
print("\nOperator: * (Multiplication)\nDescription: Multiplies two operands\nExample: 5 * 3 =", 5 * 3)
print("\nOperator: / (Division - float)\nDescription: Divides the first operand by the second and returns a floating-point number\nExample: 5 / 3 =", 5 / 3)
print("\nOperator: // (Division - floor)\nDescription: Divides the first operand by the second and returns the largest integer not greater than the result\nExample: 5 // 3 =", 5 // 3)
print("\nOperator: % (Modulus)\nDescription: Returns the remainder when the first operand is divided by the second\nExample: 5 % 3 =", 5 % 3)
print("\nOperator: ** (Exponentiation)\nDescription: Raises the first operand to the power of the second\nExample: 5 ** 3 =", 5 ** 3)

# Comparison Operators
print("\n--- Comparison Operators ---")
print("Operator: == (Equal to)\nDescription: Checks if two operands are equal\nExample: 5 == 3:", 5 == 3)
print("\nOperator: != (Not equal to)\nDescription: Checks if two operands are not equal\nExample: 5 != 3:", 5 != 3)
print("\nOperator: > (Greater than)\nDescription: Checks if the left operand is greater than the right\nExample: 5 > 3:", 5 > 3)
print("\nOperator: < (Less than)\nDescription: Checks if the left operand is less than the right\nExample: 5 < 3:", 5 < 3)
print("\nOperator: >= (Greater than or equal to)\nDescription: Checks if the left operand is greater than or equal to the right\nExample: 5 >= 3:", 5 >= 3)
print("\nOperator: <= (Less than or equal to)\nDescription: Checks if the left operand is less than or equal to the right\nExample: 5 <= 3:", 5 <= 3)

# Logical Operators
print("\n--- Logical Operators ---")
print("Operator: and (Logical AND)\nDescription: Returns True if both operands are true\nExample: (5 > 3) and (5 > 4):", (5 > 3) and (5 > 4))
print("\nOperator: or (Logical OR)\nDescription: Returns True if at least one of the operands is true\nExample: (5 > 3) or (5 < 4):", (5 > 3) or (5 < 4))
print("\nOperator: not (Logical NOT)\nDescription: Reverses the logical state of the operand\nExample: not (5 > 3):", not (5 > 3))

# Bitwise Operators
print("\n--- Bitwise Operators ---")
print("Operator: & (Bitwise AND)\nDescription: Sets each bit to 1 if both bits are 1.\nExample: 5 & 3 =", 5 & 3)
print("Operator: | (Bitwise OR)\nDescription: Sets each bit to 1 if one of two bits is 1.\nExample: 5 | 3 =", 5 | 3)
print("Operator: ^ (Bitwise XOR)\nDescription: Sets each bit to 1 if only one of two bits is 1.\nExample: 5 ^ 3 =", 5 ^ 3)
print("Operator: ~ (Bitwise NOT)\nDescription: Inverts all the bits.\nExample: ~5 =", ~5)
print("Operator: << (Bitwise left shift)\nDescription: Shifts left by pushing zeros in from the right and lets the leftmost bits fall off.\nExample: 5 << 1 =", 5 << 1)
print("Operator: >> (Bitwise right shift)\nDescription: Shifts right by pushing copies of the leftmost bit in from the left, and lets the rightmost bits fall off.\nExample: 5 >> 1 =", 5 >> 1)

# Membership Operators
print("\n--- Membership Operators ---")
print("Operator: in\nDescription: Evaluates to True if it finds a variable in the specified sequence and False otherwise.\nExample: 'Hello' in 'Hello World':", 'Hello' in 'Hello World')
print("Operator: not in\nDescription: Evaluates to True if it does not find a variable in the specified sequence and False otherwise.\nExample: 'Goodbye' not in 'Hello World':", 'Goodbye' not in 'Hello World')

# Identity Operators
print("\n--- Identity Operators ---")
print("Operator: is\nDescription: Evaluates to True if the variables on either side of the operator point to the same object and False otherwise.\nExample: [] is []:", [] is [])
print("Operator: is not\nDescription: Evaluates to True if the variables on either side of the operator do not point to the same object and False otherwise.\nExample: [] is not []:", [] is not [])


# Assignment Operators
print("\n--- Assignment Operators ---")
print("Operator: =\nDescription: Assigns a value to a variable.\nExample: x = 5")
x = 5
print("Result:", x)

print("\nOperator: +=\nDescription: Adds the right operand to the left operand and assigns the result to the left operand.\nExample: x = 5; x += 3")
x = 5; x += 3
print("Result:", x)

print("\nOperator: -=\nDescription: Subtracts the right operand from the left operand and assigns the result to the left operand.\nExample: x = 8; x -= 3")
x = 8; x -= 3
print("Result:", x)

print("\nOperator: *=\nDescription: Multiplies the right operand with the left operand and assigns the result to the left operand.\nExample: x = 5; x *= 3")
x = 5; x *= 3
print("Result:", x)

print("\nOperator: /=\nDescription: Divides the left operand by the right operand and assigns the result to the left operand.\nExample: x = 15; x /= 3")
x = 15; x /= 3
print("Result:", x)

print("\nOperator: %=\nDescription: Takes modulus using two operands and assigns the result to the left operand.\nExample: x = 19; x %= 4")
x = 19; x %= 4
print("Result:", x)

print("\nOperator: //=\nDescription: Performs floor division on operands and assigns the result to the left operand.\nExample: x = 17; x //= 4")
x = 17; x //= 4
print("Result:", x)

print("\nOperator: **=\nDescription: Performs exponential calculation on operators and assigns the result to the left operand.\nExample: x = 5; x **= 3")
x = 5; x **= 3
print("Result:", x)

print("\nOperator: &=\nDescription: Performs bitwise AND on operands and assigns the result to the left operand.\nExample: x = 5; x &= 3")
x = 5; x &= 3
print("Result:", x)

print("\nOperator: |=\nDescription: Performs bitwise OR on operands and assigns the result to the left operand.\nExample: x = 5; x |= 3")
x = 5; x |= 3
print("Result:", x)

print("\nOperator: ^=\nDescription: Performs bitwise XOR on operands and assigns the result to the left operand.\nExample: x = 5; x ^= 3")
x = 5; x ^= 3
print("Result:", x)

print("\nOperator: >>=\nDescription: Performs bitwise right shift on operands and assigns the result to the left operand.\nExample: x = 20; x >>= 3")
x = 20; x >>= 3
print("Result:", x)

print("\nOperator: <<=\nDescription: Performs bitwise left shift on operands and assigns the result to the left operand.\nExample: x = 5; x <<= 3")
x = 5; x <<= 3
print("Result:", x)
