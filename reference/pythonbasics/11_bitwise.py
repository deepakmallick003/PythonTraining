from scripts.common import *

# Bitwise AND (&) - Specific Scenario Questions
def bitwise_and_questions():
    print("\n--- Bitwise AND (&) Questions ---")

    def common_security_features(product1, product2):
        return product1 & product2

    print("\nQuestion: : Given two security products with feature codes, find the common features.")
    print_function(common_security_features)
    print("\nOutput:", common_security_features(12, 10))

    def mask_sensitive_data(data, mask):
        return data & mask

    print("\nQuestion: : Mask sensitive data using a specific pattern.")
    print_function(mask_sensitive_data)
    print("\nOutput:", mask_sensitive_data(15, 6))


# Bitwise OR (|) - Specific Scenario Questions
def bitwise_or_questions():
    print("\n--- Bitwise OR (|) Questions ---")

    def combine_permissions(user, group):
        return user | group

    print("\nQuestion: : Combine user and group permissions into a single permission set.")
    print_function(combine_permissions)
    print("\nOutput:", combine_permissions(9, 4))

    def activate_features(current, new):
        return current | new

    print("\nQuestion: : Activate new features in a system without altering existing ones.")
    print_function(activate_features)
    print("\nOutput:", activate_features(2, 5))


# Bitwise XOR (^) - Specific Scenario Questions
def bitwise_xor_questions():
    print("\n--- Bitwise XOR (^) Questions ---")

    def toggle_system_modes(current_mode, toggle):
        return current_mode ^ toggle

    print("\nQuestion: : Toggle specific system modes using a toggle code.")
    print_function(toggle_system_modes)
    print("\nOutput:", toggle_system_modes(14, 9))

    def encrypt_decrypt_data(data, key):
        return data ^ key

    print("\nQuestion: : Simple encryption/decryption of data using XOR.")
    print_function(encrypt_decrypt_data)
    print("\nOutput:", encrypt_decrypt_data(5, 0b1111))


# Bitwise NOT (~) - Specific Scenario Questions
def bitwise_not_questions():
    print("\n--- Bitwise NOT (~) Questions ---")

    def invert_display_settings(settings):
        return ~settings & 0b1111  # Assuming 4-bit settings for clarity

    print("\nQuestion: : Invert display settings for a dark/light mode toggle.")
    print_function(invert_display_settings)
    print("\nOutput:", invert_display_settings(4))

    def find_complement_number(number):
        return ~number & 0b1111

    print("\nQuestion: : Find the 4-bit complement of a given number.")
    print_function(find_complement_number)
    print("\nOutput:", find_complement_number(3))



bitwise_and_questions()
bitwise_or_questions()
bitwise_xor_questions()
bitwise_not_questions()
