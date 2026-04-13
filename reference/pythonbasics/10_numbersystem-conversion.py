# This Python script illustrates number system conversions in Python.

# Decimal to Binary
print("\n--- Decimal to Binary ---")
print("Decimal is base-10 (0-9). Binary is base-2 (0-1).")
print("In binary, each digit represents a power of 2, starting from 2^0 from right.")
decimal_number = 5
binary_number = bin(decimal_number)
print("Decimal:", decimal_number, "-> Binary:", binary_number)

# Binary to Decimal
print("\n--- Binary to Decimal ---")
print("Converting binary to decimal involves multiplying each bit by its corresponding power of 2 and summing the results.")
binary_number = '0b101'  # Binary representation of 5
decimal_number = int(binary_number, 2)
print("Binary:", binary_number, "-> Decimal:", decimal_number)

# Decimal to Hexadecimal
print("\n--- Decimal to Hexadecimal ---")
print("Hexadecimal is base-16 (0-9 and A-F). Each digit represents a power of 16.")
decimal_number = 255
hexadecimal_number = hex(decimal_number)
print("Decimal:", decimal_number, "-> Hexadecimal:", hexadecimal_number)

# Hexadecimal to Decimal
print("\n--- Hexadecimal to Decimal ---")
print("Converting hexadecimal to decimal involves multiplying each digit by its corresponding power of 16 and summing the results.")
hexadecimal_number = '0xff'  # Hexadecimal representation of 255
decimal_number = int(hexadecimal_number, 16)
print("Hexadecimal:", hexadecimal_number, "-> Decimal:", decimal_number)

# Decimal to Octal
print("\n--- Decimal to Octal ---")
print("Octal is base-8 (0-7). Each digit represents a power of 8.")
decimal_number = 64
octal_number = oct(decimal_number)
print("Decimal:", decimal_number, "-> Octal:", octal_number)

# Octal to Decimal
print("\n--- Octal to Decimal ---")
print("Converting octal to decimal involves multiplying each digit by its corresponding power of 8 and summing the results.")
octal_number = '0o100'  # Octal representation of 64
decimal_number = int(octal_number, 8)
print("Octal:", octal_number, "-> Decimal:", decimal_number)

# Print a separator for readability
print("\n" + "-" * 50 + "\n")
