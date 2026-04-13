# Operator Precedence Questions in Python

# Question 1
print("\n--- Question 1 ---")
print("Question: 3 + 4 * 5")
print("Description: Multiplication (*) has higher precedence than addition (+).")
print("Answer:", 3 + 4 * 5)

# Question 2
print("\n--- Question 2 ---")
print("Question: (3 + 4) * 5")
print("Description: Parentheses alter the natural precedence, making addition (+) evaluated before multiplication (*).")
print("Answer:", (3 + 4) * 5)

# Question 3
print("\n--- Question 3 ---")
print("Question: -3 ** 2")
print("Description: Exponentiation (**) has higher precedence than unary minus (-).")
print("Answer:", -3 ** 2)

# Question 4
print("\n--- Question 4 ---")
print("Question: 10 / 2 * 3")
print("Description: Division (/) and multiplication (*) have the same precedence and are evaluated left to right.")
print("Answer:", 10 / 2 * 3)

# Question 5
print("\n--- Question 5 ---")
print("Question: 4 ** 2 ** 3")
print("Description: Exponentiation (**) is right associative.")
print("Answer:", 4 ** 2 ** 3)

# Question 6
print("\n--- Question 6 ---")
print("Question: 5 > 3 and 4 < 7")
print("Description: Comparison operators have higher precedence than logical operators.")
print("Answer:", 5 > 3 and 4 < 7)

# Question 7
print("\n--- Question 7 ---")
print("Question: 5 & 3 | 2")
print("Description: Bitwise AND (&) has higher precedence than bitwise OR (|).")
print("Answer:", 5 & 3 | 2)

# Question 8
print("\n--- Question 8 ---")
print("Question: 2 + 3 << 2")
print("Description: Bitwise shift (<<) has lower precedence than addition (+).")
print("Answer:", 2 + 3 << 2)

# Question 9
print("\n--- Question 9 ---")
print("Question: not True or False")
print("Description: Logical NOT (not) has higher precedence than logical OR (or).")
print("Answer:", not True or False)

# Question 10
print("\n--- Question 10 ---")
print("Question: True == (not False)")
print("Description: Logical NOT (not) has higher precedence than comparison (==). Parentheses ensure the 'not' operation is evaluated first.")
print("Answer:", True == (not False))

# Question 11
print("\n--- Question 11 ---")
print("Question: 2 + 3 * 4 - 5")
print("Description: Multiplication (*) has higher precedence than addition (+) and subtraction (-).")
print("Answer:", 2 + 3 * 4 - 5)

# Question 12
print("\n--- Question 12 ---")
print("Question: 4 | 2 & 3")
print("Description: Bitwise AND (&) has higher precedence than bitwise OR (|).")
print("Answer:", 4 | 2 & 3)

# Question 13
print("\n--- Question 13 ---")
print("Question: ~4 + 3")
print("Description: Bitwise NOT (~) has higher precedence than arithmetic operators like addition (+).")
print("Answer:", ~4 + 3)

# Question 14
print("\n--- Question 14 ---")
print("Question: 3 < 4 and 5 >= 2 or 6 != 7")
print("Description: Comparison operators have higher precedence than logical operators (and, or).")
print("Answer:", 3 < 4 and 5 >= 2 or 6 != 7)

# Question 15
print("\n--- Question 15 ---")
print("Question: 5 * 3 >> 2")
print("Description: Arithmetic multiplication (*) has higher precedence than bitwise right shift (>>).")
print("Answer:", 5 * 3 >> 2)

# Question 16
print("\n--- Question 16 ---")
print("Question: 3 ** 2 * 4")
print("Description: Exponentiation (**) has higher precedence than multiplication (*).")
print("Answer:", 3 ** 2 * 4)

# Question 17
print("\n--- Question 17 ---")
print("Question: 4 + 5 << 3 - 2")
print("Description: Arithmetic operators (+, -) have higher precedence than bitwise shift (<<).")
print("Answer:", 4 + 5 << 3 - 2)

# Question 18
print("\n--- Question 18 ---")
print("Question: 7 & 5 | 3 ^ 2")
print("Description: Bitwise AND (&) and XOR (^) have higher precedence than bitwise OR (|).")
print("Answer:", 7 & 5 | 3 ^ 2)

# Question 19
print("\n--- Question 19 ---")
print("Question: (3 + 4) * 5 ^ 2")
print("Description: Parentheses alter precedence; followed by exponentiation (^), then multiplication (*).")
print("Answer:", (3 + 4) * 5 ^ 2)

# Question 20
print("\n--- Question 20 ---")
print("Question: -3 * 2 + 7 // 2")
print("Description: Unary minus (-) has higher precedence than multiplication (*), division (//), and addition (+).")
print("Answer:", -3 * 2 + 7 // 2)

# Comparison Operators Precedence Questions in Python

# Question 21
print("\n--- Question 21 ---")
print("Question: 2 + 3 > 5 - 1")
print("Description: Arithmetic operators (+, -) are evaluated before comparison operators (>).")
print("Answer:", 2 + 3 > 5 - 1)

# Question 22
print("\n--- Question 22 ---")
print("Question: 4 * 3 == 2 ** 3")
print("Description: Arithmetic operators (*, **) are evaluated before the equality operator (==).")
print("Answer:", 4 * 3 == 2 ** 3)

# Question 23
print("\n--- Question 23 ---")
print("Question: 7 // 3 != 2 | 1")
print("Description: Arithmetic division (//) and bitwise OR (|) are evaluated before the non-equality operator (!=).")
print("Answer:", 7 // 3 != 2 | 1)

# Question 24
print("\n--- Question 24 ---")
print("Question: 5 <= 3 + 2 and 4 >= 2 * 2")
print("Description: Arithmetic operators (+, *) are evaluated before comparison operators (<=, >=) and logical AND (and).")
print("Answer:", 5 <= 3 + 2 and 4 >= 2 * 2)

# Question 25
print("\n--- Question 25 ---")
print("Question: 6 % 3 == 0 or 5 // 2 == 2")
print("Description: Modulus (%) and floor division (//) are evaluated before equality (==) and logical OR (or).")
print("Answer:", 6 % 3 == 0 or 5 // 2 == 2)
