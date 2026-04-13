def explain_continue():
    print("\n--- Explain Continue ---")
    print("The 'continue' statement skips the current iteration of a loop and proceeds to the next iteration.")

    for i in range(5):
        if i == 2:
            continue
        print(i)

def explain_pass():
    print("\n--- Explain Pass ---")
    print("The 'pass' statement is a null operation; it's a placeholder used when a statement is syntactically required but you don't want any command or code to execute.")

    for i in range(5):
        if i == 2:
            pass
        print(i)

explain_continue()
explain_pass()
