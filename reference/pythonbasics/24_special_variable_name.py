from scripts.common import *


print("""
Starting Point of Execution:

__main__ is the starting point in Python. When a script is run directly, its __name__ is set to "__main__".
Special Variable __name__:

A built-in variable that represents the name of the current module.
Its value changes depending on how the script is being used.
Behavior of __name__:

If a file is run as a main program, __name__ equals "__main__".
If the file is imported as a module in another script, __name__ equals the name of the module (file name).
Use of __name__ in Scripts:

Helps in differentiating between when a script is run directly or imported as a module.
Controls which parts of the code to execute depending on the context.

""")


print("Common Usage Pattern:")
if __name__ == "__main__":
    # Code here runs only when the script is executed directly
    pass