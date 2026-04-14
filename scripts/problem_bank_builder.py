#!/usr/bin/env python3
"""
Builds the editable problem bank from the reference/pythonbasics source files.

The generated storage is runtime data. The Flask app should read only from the
problem bank, not from the reference folder directly.
"""

from __future__ import annotations

import ast
import builtins
import copy
import json
import re
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parent.parent
REFERENCE_DIR = BASE_DIR / "reference" / "pythonbasics"
REFERENCE_ALGOS_DIR = BASE_DIR / "reference" / "algos"
PROBLEM_BANK_DIR = BASE_DIR / "app" / "problem_bank"
PROBLEM_BANK_CATEGORIES_DIR = PROBLEM_BANK_DIR / "categories"

BUILTIN_NAMES = set(dir(builtins))

CATEGORY_NAME_MAP = {
    "01_strings.py": "Strings",
    "02_list.py": "Lists",
    "03_tuple.py": "Tuples",
    "04_set.py": "Sets",
    "05_dictionary.py": "Dictionaries",
    "06_variables.py": "Variables",
    "07_datatypes.py": "Data Types",
    "08_operators.py": "Operators",
    "09_operators-precedence.py": "Operator Precedence",
    "10_numbersystem-conversion.py": "Number System Conversion",
    "11_bitwise.py": "Bitwise",
    "12_user-input.py": "User Input",
    "13_loop-breakers.py": "Loop Breakers",
    "14_arrays.py": "Arrays",
    "15_numpy-1.py": "NumPy 1",
    "16_numpy-2.py": "NumPy 2",
    "17_numpy_matrix.py": "NumPy Matrix",
    "18_functions-argument-types.py": "Function Argument Types",
    "19_function-global-keyword.py": "Function Global Keyword",
    "20_functions-mutable-immutable.py": "Functions Mutable vs Immutable",
    "21_lambda.py": "Lambda",
    "22_decorator.py": "Decorator",
    "23_underscore-and-dunder.py": "Underscore and Dunder",
    "24_special_variable_name.py": "Special Variable __name__",
    "25_methodtypes.py": "Method Types",
    "26_innerclass.py": "Inner Class",
    "27_inheritance_types.py": "Inheritance Types",
    "28_inheritance_order.py": "Inheritance Order",
    "29_polymorphism-ducktyping.py": "Polymorphism and Duck Typing",
}

TITLE_FROM_FILENAME_MAP = {
    "22_decorator.py": "Smart Division Decorator",
    "24_special_variable_name.py": "The __name__ Guard",
    "25_methodtypes.py": "Instance, Class, and Static Methods",
    "26_innerclass.py": "Student with Nested Laptop Class",
    "28_inheritance_order.py": "Method Resolution Order",
}

PROMPT_OVERRIDES = {
    "06_variables.py": {
        "Concept 1: Variables And Memory": "Inside main(), assign `x = 10`, copy it into `y`, then reassign `x = 15`. Print the values and object identities with `id()` to show that rebinding `x` does not change `y`.",
        "Concept 2: Garbage Collection": "Inside main(), assign `z = 20`, print its identity with `id()`, then reassign `z = 25` and print the new identity. Use the output to demonstrate how Python can discard objects that are no longer referenced.",
        "Concept 3: Constants And Types": "Inside main(), demonstrate three ideas: print the type of a constant like `PI`, create a simple `Car` object and print its type, and show that two list variables can reference the same list by mutating one and printing both.",
    },
    "07_datatypes.py": {
        "Nonetype": "Inside main(), assign `a = None`, then print the value and its type to show how Python represents the absence of a value.",
        "Numbers": "Inside main(), create one integer, one float, and one complex number. Print each value and its type so the learner can compare the three numeric data types.",
        "Type Conversion": "Inside main(), convert a float to an int, convert that int back to a float, and create a complex number. Print each converted value together with its type.",
        "Booleans": "Inside main(), store `True` in one variable and evaluate `3 < 5` in another. Print both values and their types to show how booleans work in Python.",
        "Sequence Data Types": "Inside main(), print a short explanation that lists the common sequence-style containers shown in this lesson: list, tuple, set, string, and range.",
        "List": "Inside main(), create the sample list `lst = [25, 36, 45, 12]`, then print the list and its type.",
        "Tuple": "Inside main(), create the sample tuple `t = (25, 36, 45, 12, 7)`, then print the tuple and its type.",
        "Set": "Inside main(), create the sample set `{25, 36, 45, 12, 25, 36}` and print the resulting set and its type so the learner can see that duplicates are removed.",
        "String": "Inside main(), assign `str_val = \"hello\"`, then print the string and its type.",
        "Range": "Inside main(), create `r = range(10)`, print the range object and its type, then print `list(range(2, 10, 2))` to show the generated values.",
        "Dictionary": "Inside main(), create the sample dictionaries, then print the dictionary, its type, its keys, its values, direct access with `['rahul']`, and access with `.get('kiran')`.",
    },
    "08_operators.py": {
        "Arithmetic Operators": "Inside main(), print worked examples for the arithmetic operators `+`, `-`, `*`, `/`, `//`, `%`, and `**` using the numbers `5` and `3`.",
        "Comparison Operators": "Inside main(), print worked examples for the comparison operators `==`, `!=`, `>`, `<`, `>=`, and `<=` using the numbers `5` and `3`.",
        "Logical Operators": "Inside main(), print worked examples for `and`, `or`, and `not` using boolean expressions based on `5`, `3`, and `4`.",
        "Bitwise Operators": "Inside main(), print worked examples for the bitwise operators `&`, `|`, `^`, `~`, `<<`, and `>>` using `5` and `3`.",
        "Membership Operators": "Inside main(), print worked examples that show how `in` and `not in` behave with the strings `'Hello'`, `'Goodbye'`, and `'Hello World'`.",
        "Identity Operators": "Inside main(), print worked examples that show the difference between `is` and `is not` using two separate empty lists.",
        "Assignment Operators": "Inside main(), demonstrate assignment operators by updating `x` step by step and printing the result after each one: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `//=`, `**=`, `&=`, `|=`, `^=`, `>>=`, and `<<=`.",
    },
    "10_numbersystem-conversion.py": {
        "Decimal To Binary": "Inside main(), convert `decimal_number = 5` to binary using `bin()` and print the labeled result.",
        "Binary To Decimal": "Inside main(), convert `binary_number = '0b101'` to decimal using `int(..., 2)` and print the labeled result.",
        "Decimal To Hexadecimal": "Inside main(), convert `decimal_number = 255` to hexadecimal using `hex()` and print the labeled result.",
        "Hexadecimal To Decimal": "Inside main(), convert `hexadecimal_number = '0xff'` to decimal using `int(..., 16)` and print the labeled result.",
        "Decimal To Octal": "Inside main(), convert `decimal_number = 64` to octal using `oct()` and print the labeled result.",
        "Octal To Decimal": "Inside main(), convert `octal_number = '0o100'` to decimal using `int(..., 8)` and print the labeled result.",
    },
    "22_decorator.py": {
        "Smart Division Decorator": "Create a `div(a, b)` function and a `smart_div` decorator. The decorator should swap the numbers when `a < b`, then call the original function so dividing `2` and `4` still prints the result of `4 / 2`.",
    },
    "23_underscore-and-dunder.py": {
        "Single Underscore for Internal Use": "Create a `Car` class with an internal `_engine_type` attribute and a `start()` method. Inside main(), instantiate the class and print both the start message and the internal attribute to demonstrate the underscore convention.",
        "Single Underscore as an Ignored Variable": "Use `_` as the ignored loop variable in a `for` loop and print `Hello!` five times inside main().",
        "Double Underscore Name Mangling": "Create `Vehicle` and `Car` classes to demonstrate double-underscore name mangling. Print the parent identification value and the child-specific identification value to show that they stay separate.",
        "Dunder Special Methods": "Create a `Book` class with `__init__` and `__str__`. Inside main(), instantiate a book and print it so Python uses the custom string representation.",
        "Module __name__ Value": "Inside main(), print the module `__name__` value so the learner can see what Python sets for the current module.",
    },
    "24_special_variable_name.py": {
        "The __name__ Guard": "Inside main(), print a short explanation of the `__name__` variable and show the common `if __name__ == \"__main__\":` guard pattern.",
    },
    "25_methodtypes.py": {
        "Instance, Class, and Static Methods": "Create a `Student` class with three marks, an `avg()` instance method, a `get_school()` class method, and an `info()` static method. Inside main(), create a student, print the average, print the school name, and call the static method.",
    },
    "26_innerclass.py": {
        "Student with Nested Laptop Class": "Create a `Student` class that owns a nested `Laptop` class. Inside main(), create a student object and print the student details followed by the laptop brand, CPU, and RAM.",
    },
    "28_inheritance_order.py": {
        "Method Resolution Order": "Create classes `A`, `B`, `C`, and `D` where `D` inherits from `B` and `C`. Use `super()` inside each constructor so instantiating `D()` prints the constructor call order and demonstrates Python's method resolution order.",
    },
    "29_polymorphism-ducktyping.py": {
        "Save Data with Duck Typing": "Create two saver classes that both expose a `save(data)` method. Inside main(), write a helper that accepts any saver object, then call it once with a file saver and once with a console saver to demonstrate duck typing.",
        "Compose with Any Writer": "Create two classes, `Pen` and `Keyboard`, that both implement `write()`. Inside main(), pass each one into a shared `compose()` function and print the output from both objects.",
        "Runtime Type Checking with hasattr": "Create a `Dog` class with `bark()` and a `pet_speak()` helper that checks for `bark()` using `hasattr`. Inside main(), call it once with a dog and once with a string to show both branches.",
        "Error Potential When Methods Are Missing": "Create a `Car` class with `drive()` and a `start_trip()` helper that expects any object passed to it to implement `drive()`. Inside main(), show the successful car call and then catch and print the `AttributeError` raised by passing a plain string.",
        "hasattr and getattr in Practice": "Create a `Calculator` class with a `calculate()` method and a helper that uses `hasattr()` and `getattr()` to call an operation by name. Inside main(), demonstrate one supported operation and one unsupported one.",
    },
}

INTERNAL_NOTE_PREFIXES = (
    "Stored as a standalone",
    "This section is stored as",
    "This category uses standalone",
    "This problem is stored as",
    "Stored as a runnable standalone",
)

ALGO_CATEGORY_CONFIG = {
    "searching": {"id": "algos-searching", "name": "Searching Algorithms", "sequence": 30},
    "sorting": {"id": "algos-sorting", "name": "Sorting Algorithms", "sequence": 31},
    "graph": {"id": "algos-graph", "name": "Graph Algorithms", "sequence": 32},
    "dp": {"id": "algos-dp", "name": "Dynamic Programming", "sequence": 33},
    "greedy": {"id": "algos-greedy", "name": "Greedy Algorithms", "sequence": 34},
    "string": {"id": "algos-string", "name": "String Algorithms", "sequence": 35},
    "backtracking": {"id": "algos-backtracking", "name": "Backtracking Algorithms", "sequence": 36},
    "maths": {"id": "algos-maths", "name": "Math Algorithms", "sequence": 37},
    "misc": {"id": "algos-recursion", "name": "Recursion Foundations", "sequence": 38},
}

ALGO_PROMPT_BY_GROUP = {
    "searching": "Implement {title} inside main() using the sample array and target shown below, then print the search result in the same format as the example.",
    "sorting": "Implement {title} inside main() using the sample input shown below, then print the sorted result in the same format as the example.",
    "graph": "Implement {title} inside main() using the sample graph shown below, then print the traversal, path summary, or distance table in the same format as the example.",
    "dp": "Implement {title} inside main() using the sample input shown below, then print the computed dynamic-programming result in the same format as the example.",
    "greedy": "Implement {title} inside main() using the sample input shown below, then print the greedy algorithm result in the same format as the example.",
    "string": "Implement {title} inside main() using the sample text or pattern shown below, then print the string-processing result in the same format as the example.",
    "backtracking": "Implement {title} inside main() using the sample board or input shown below, then print the constructed solution in the same format as the example.",
    "maths": "Implement {title} inside main() using the sample values shown below, then print the mathematical result in the same format as the example.",
    "misc": "Implement {title} inside main() using the sample values shown below, then print the computed result or generated sequence in the same format as the example.",
}

ALGO_SOURCE_FALLBACKS = {
    "48_string_boyer-moore.py": """
def create_bad_char_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern):
        table[char] = max(1, length - index - 1)
    return table


def boyer_moore_search(text, pattern):
    bad_char_table = create_bad_char_table(pattern)
    text_index = 0
    pattern_length = len(pattern)
    text_length = len(text)
    matches = []

    while text_index <= text_length - pattern_length:
        scan_index = pattern_length - 1
        while scan_index >= 0 and pattern[scan_index] == text[text_index + scan_index]:
            scan_index -= 1
        if scan_index < 0:
            matches.append(text_index)
            text_index += pattern_length
        else:
            shift = bad_char_table.get(text[text_index + scan_index], pattern_length)
            text_index += max(1, shift)

    return matches


def main():
    text = "HERE IS A SIMPLE EXAMPLE"
    pattern = "EXAMPLE"
    matches = boyer_moore_search(text, pattern)
    print("Text:", text)
    print("Pattern:", pattern)
    print("Match indices:", matches)


if __name__ == "__main__":
    main()
""".strip(),
    "06_searching_exponential-search.py": """
def binary_search(arr, left, right, target):
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def exponential_search(arr, target):
    if not arr:
        return -1
    if arr[0] == target:
        return 0

    index = 1
    while index < len(arr) and arr[index] <= target:
        index *= 2

    return binary_search(arr, index // 2, min(index, len(arr) - 1), target)


def main():
    arr = [2, 3, 4, 10, 40, 55, 78, 91]
    targetVal = 78
    result = exponential_search(arr, targetVal)
    if result != -1:
        print("Value", targetVal, "found at index", result)
    else:
        print("Value", targetVal, "not found")


if __name__ == "__main__":
    main()
""".strip(),
    "49_string_z-algorithm.py": """
def z_algorithm(text):
    z = [0] * len(text)
    left = right = 0
    for i in range(1, len(text)):
        if i <= right:
            z[i] = min(right - i + 1, z[i - left])
        while i + z[i] < len(text) and text[z[i]] == text[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1
    return z


def main():
    text = "aabxaabxcaabxaabxay"
    z_values = z_algorithm(text)
    print("Text:", text)
    print("Z-array:", z_values)


if __name__ == "__main__":
    main()
""".strip(),
    "50_string_aho-korasick.py": """
from collections import deque


class Node:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []


def build_automaton(patterns):
    root = Node()
    for pattern in patterns:
        current = root
        for char in pattern:
            current = current.children.setdefault(char, Node())
        current.output.append(pattern)

    queue = deque()
    for child in root.children.values():
        child.fail = root
        queue.append(child)

    while queue:
        current = queue.popleft()
        for char, child in current.children.items():
            queue.append(child)
            fallback = current.fail
            while fallback and char not in fallback.children:
                fallback = fallback.fail
            child.fail = fallback.children[char] if fallback and char in fallback.children else root
            child.output.extend(child.fail.output)
    return root


def aho_corasick_search(text, patterns):
    root = build_automaton(patterns)
    current = root
    matches = []

    for index, char in enumerate(text):
        while current and char not in current.children:
            current = current.fail
        current = current.children[char] if current and char in current.children else root
        for pattern in current.output:
            matches.append((pattern, index - len(pattern) + 1))

    return matches


def main():
    text = "ahishers"
    patterns = ["he", "she", "hers", "his"]
    matches = aho_corasick_search(text, patterns)
    print("Text:", text)
    print("Patterns:", patterns)
    print("Matches:", matches)


if __name__ == "__main__":
    main()
""".strip(),
    "51_string_manachers.py": """
def longest_palindromic_substring(text):
    transformed = "^#" + "#".join(text) + "#$"
    radius = [0] * len(transformed)
    center = right = 0

    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i
        if i < right:
            radius[i] = min(right - i, radius[mirror])

        while transformed[i + 1 + radius[i]] == transformed[i - 1 - radius[i]]:
            radius[i] += 1

        if i + radius[i] > right:
            center = i
            right = i + radius[i]

    max_len = max(radius)
    center_index = radius.index(max_len)
    start = (center_index - max_len) // 2
    return text[start:start + max_len]


def main():
    text = "forgeeksskeegfor"
    result = longest_palindromic_substring(text)
    print("Text:", text)
    print("Longest palindromic substring:", result)


if __name__ == "__main__":
    main()
""".strip(),
    "55_backtracking_knight-tour.py": """
MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1),
]


def is_valid(row, col, n, board):
    return 0 <= row < n and 0 <= col < n and board[row][col] == -1


def onward_count(row, col, n, board):
    return sum(1 for dr, dc in MOVES if is_valid(row + dr, col + dc, n, board))


def knight_tour(n, start_row=0, start_col=0):
    board = [[-1 for _ in range(n)] for _ in range(n)]
    board[start_row][start_col] = 0
    row, col = start_row, start_col

    for step in range(1, n * n):
        candidates = []
        for dr, dc in MOVES:
            next_row = row + dr
            next_col = col + dc
            if is_valid(next_row, next_col, n, board):
                candidates.append((onward_count(next_row, next_col, n, board), next_row, next_col))

        if not candidates:
            return None

        _, row, col = min(candidates)
        board[row][col] = step

    return board


def main():
    n = 5
    board = knight_tour(n)
    if board is None:
        print("No tour found.")
        return
    for row in board:
        print(" ".join(f"{cell:2d}" for cell in row))


if __name__ == "__main__":
    main()
""".strip(),
}


@dataclass
class ProblemRecord:
    title: str
    prompt: str
    sequence: int
    starter_code: str
    solution: str
    test_cases: list[dict] = field(default_factory=list)
    examples: list[dict] = field(default_factory=list)
    difficulty: str = "Easy"
    notes: list[str] = field(default_factory=list)
    source_reference: dict = field(default_factory=dict)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def category_meta(path: Path) -> dict:
    stem = path.stem
    sequence = int(stem.split("_", 1)[0])
    category_name = CATEGORY_NAME_MAP.get(path.name, stem.replace("_", " ").title())
    category_id = slugify(re.sub(r"^\d+[_-]?", "", stem))
    return {
        "id": category_id,
        "name": category_name,
        "sequence": sequence,
        "source_reference": path.name,
    }


def pretty_name(value: str) -> str:
    value = value.replace("\\n", " ").replace("\\t", " ")
    value = value.replace("_", " ").replace("-", " ").strip()
    return re.sub(r"\s+", " ", value).title()


def node_to_source(node: ast.AST) -> str:
    return ast.unparse(node).strip()


def nodes_to_source(nodes: Iterable[ast.AST]) -> str:
    return "\n\n".join(node_to_source(node) for node in nodes if node_to_source(node))


def is_print_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "print"
    )


def is_print_function_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "print_function"
    )


def first_print_text(node: ast.AST) -> str | None:
    if not is_print_call(node):
        return None
    call = node.value
    if not call.args:
        return None
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value
    return None


def import_lines_from_source(code: str) -> list[str]:
    try:
        module = ast.parse(code)
    except SyntaxError:
        return []
    lines = []
    for node in module.body:
        if isinstance(node, ast.Import):
            lines.append(node_to_source(node))
        elif isinstance(node, ast.ImportFrom):
            if node.module == "scripts.common":
                continue
            lines.append(node_to_source(node))
    return lines


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def split_imports_and_body(code: str) -> tuple[list[str], str]:
    try:
        module = ast.parse(code)
    except SyntaxError:
        return [], code.strip()

    import_nodes = []
    body_nodes = []
    for node in module.body:
        if isinstance(node, ast.Import):
            import_nodes.append(node_to_source(node))
        elif isinstance(node, ast.ImportFrom):
            if node.module == "scripts.common":
                continue
            import_nodes.append(node_to_source(node))
        else:
            body_nodes.append(node)
    return import_nodes, nodes_to_source(body_nodes).strip()


def extract_main_guard_body(node: ast.If) -> list[ast.stmt] | None:
    test = node.test
    if not (
        isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and len(test.comparators) == 1
        and isinstance(test.comparators[0], ast.Constant)
        and test.comparators[0].value == "__main__"
    ):
        return None
    return node.body


def split_runnable_script(source: str) -> tuple[list[str], str, str]:
    try:
        module = ast.parse(source)
    except SyntaxError:
        import_lines, action_body = split_imports_and_body(source)
        return import_lines, "", action_body

    import_lines: list[str] = []
    support_nodes: list[ast.AST] = []
    main_body_nodes: list[ast.AST] | None = None

    for node in module.body:
        if isinstance(node, ast.Import):
            import_lines.append(node_to_source(node))
            continue
        if isinstance(node, ast.ImportFrom):
            if node.module == "scripts.common":
                continue
            import_lines.append(node_to_source(node))
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            main_body_nodes = list(node.body)
            continue
        if isinstance(node, ast.If):
            guard_body = extract_main_guard_body(node)
            if guard_body is not None:
                continue
        support_nodes.append(node)

    if main_body_nodes is None:
        return dedupe_preserve_order(import_lines), "", nodes_to_source(support_nodes).strip()

    return (
        dedupe_preserve_order(import_lines),
        nodes_to_source(support_nodes).strip(),
        nodes_to_source(main_body_nodes).strip(),
    )


def indent_block(text: str, spaces: int = 4) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else "" for line in text.splitlines())


def extract_parameter_names_from_setup(setup_source: str) -> list[str]:
    if not setup_source.strip():
        return []

    try:
        nodes = ast.parse(setup_source).body
    except SyntaxError:
        return []

    ordered_names: list[str] = []
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                for name in extract_target_names(target):
                    if name not in ordered_names:
                        ordered_names.append(name)
        elif isinstance(node, ast.AnnAssign):
            for name in extract_target_names(node.target):
                if name not in ordered_names:
                    ordered_names.append(name)
        elif isinstance(node, ast.AugAssign):
            for name in extract_target_names(node.target):
                if name not in ordered_names:
                    ordered_names.append(name)
    return ordered_names


def split_support_and_input_setup(setup_source: str) -> tuple[str, str]:
    if not setup_source.strip():
        return "", ""

    try:
        module = ast.parse(setup_source)
    except SyntaxError:
        return "", setup_source.strip()

    support_nodes = []
    input_nodes = []
    support_refs: set[str] = set()
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            support_nodes.append(node)
            for child in ast.walk(node):
                if isinstance(child, ast.Name):
                    support_refs.add(child.id)
                elif isinstance(child, ast.Global):
                    support_refs.update(child.names)
                elif (
                    isinstance(child, ast.Subscript)
                    and isinstance(child.value, ast.Call)
                    and isinstance(child.value.func, ast.Name)
                    and child.value.func.id == "globals"
                    and isinstance(child.slice, ast.Constant)
                    and isinstance(child.slice.value, str)
                ):
                    support_refs.add(child.slice.value)

    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        elif isinstance(node, ast.Assign):
            target_names = set()
            for target in node.targets:
                target_names.update(extract_target_names(target))
            if target_names & support_refs:
                support_nodes.append(node)
            else:
                input_nodes.append(node)
        elif isinstance(node, ast.AnnAssign):
            target_names = extract_target_names(node.target)
            if target_names & support_refs:
                support_nodes.append(node)
            else:
                input_nodes.append(node)
        else:
            input_nodes.append(node)
    return nodes_to_source(support_nodes).strip(), nodes_to_source(input_nodes).strip()


def build_call_expression(parameter_names: list[str]) -> str:
    return f"main({', '.join(parameter_names)})" if parameter_names else "main()"


def build_wrapped_code(
    import_lines: list[str],
    support_source: str = "",
    setup_source: str = "",
    main_body: str = "",
    parameter_names: list[str] | None = None,
    placeholder: bool = False,
) -> str:
    parameter_names = parameter_names or []
    sections = []
    if import_lines:
        sections.append("\n".join(import_lines))
    if support_source.strip():
        sections.append(support_source.strip())

    signature = f"def main({', '.join(parameter_names)}):" if parameter_names else "def main():"
    body = main_body.strip()
    if placeholder or not body:
        body = "# Write your solution here.\npass" if placeholder else "pass"
    sections.append(signature + "\n" + indent_block(body))

    guard_lines = []
    if setup_source.strip():
        guard_lines.append(setup_source.strip())
    guard_lines.append(build_call_expression(parameter_names))
    guard = (
        'if __name__ == "__main__":\n'
        + indent_block("\n".join(guard_lines))
    )
    sections.append(guard)
    return "\n\n".join(section for section in sections if section).strip() + "\n"


def build_minimum_test_cases(
    input_code: str,
    expected_output: str,
    call_expression: str = "",
    minimum: int = 3,
) -> list[dict]:
    base_case = {
        "input": input_code,
        "expected_output": expected_output,
    }
    if call_expression:
        base_case["call"] = call_expression
    return [
        {
            **base_case,
            "label": f"Test {index}",
        }
        for index in range(1, minimum + 1)
    ]


def build_description(prompt: str, notes: list[str], has_tests: bool) -> str:
    prompt_text = prompt.strip().rstrip(".")
    if not prompt_text:
        prompt_text = "Complete the exercise"

    standalone_note = any("standalone" in note.lower() for note in notes)
    if has_tests:
        suffix = "Implement the logic in main(...) and match the expected output for the provided cases."
    elif standalone_note:
        suffix = "Run the snippet in main() and compare the result with the example output."
    else:
        suffix = "Use main() to produce the expected result shown in the example."
    return f"{prompt_text}. {suffix}"


def filter_user_notes(notes: list[str]) -> list[str]:
    return [
        note for note in notes
        if not any(note.startswith(prefix) for prefix in INTERNAL_NOTE_PREFIXES)
    ]


def override_prompt(path: Path, title: str, fallback: str) -> str:
    overrides = PROMPT_OVERRIDES.get(path.name, {})
    if title in overrides:
        return overrides[title]

    normalized_title = slugify(title)
    for candidate, prompt in overrides.items():
        if slugify(candidate) == normalized_title:
            return prompt
    return fallback


def fallback_example_input_from_prompt(prompt: str) -> str:
    cleaned = prompt.strip().rstrip(".")
    if not cleaned:
        return "No external input. Use the constants, expressions, and helper calls already shown in the scaffold."

    cleaned = re.sub(r"^Inside main\(\),\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^Implement\s+(.+?)\s+inside main\(\)\s*", r"\1: ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return f"Use this setup idea:\n{cleaned}"


def summarize_example_input(solution_code: str, prompt: str = "", max_lines: int = 6) -> str:
    try:
        module = ast.parse(solution_code)
    except SyntaxError:
        return fallback_example_input_from_prompt(prompt)

    body_nodes = module.body
    main_node = next(
        (node for node in body_nodes if isinstance(node, ast.FunctionDef) and node.name == "main"),
        None,
    )
    if main_node:
        body_nodes = main_node.body

    lines: list[str] = []
    for node in body_nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            lines.append(ast.unparse(node).strip())
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id == "print":
                continue
            lines.append(ast.unparse(node).strip())
        if len(lines) >= max_lines:
            break

    if not lines:
        return fallback_example_input_from_prompt(prompt)
    return "Use the sample setup:\n" + "\n".join(lines[:max_lines])


def normalize_algo_source(path: Path, source: str) -> str:
    """Patch a few reference snippets so they can execute cleanly as examples."""
    if (not source.strip() or path.name == "48_string_boyer-moore.py") and path.name in ALGO_SOURCE_FALLBACKS:
        source = ALGO_SOURCE_FALLBACKS[path.name]
    if path.name == "38_dp_travelling-salesman-problem.py":
        source = source.replace(
            "print(nearest_neighbor_tsp(graph))",
            "print(nearest_neighbor_tsp(graph, 0))",
            1,
        )
    return source


def algo_file_meta(path: Path) -> tuple[str, int, str]:
    """Return algorithm group, global order, and learner-facing title for a file."""
    match = re.match(r"^(?P<order>\d+)_(?P<group>[a-zA-Z]+)_(?P<slug>.+)\.py$", path.name)
    if match:
        group = match.group("group").lower()
        if group == "searchng":
            group = "searching"
        order = int(match.group("order"))
        title = pretty_name(match.group("slug"))
        return group, order, title

    stem = path.stem
    misc_order = {"factorial": 1, "fibonacci": 2}.get(stem, 99)
    return "misc", misc_order, pretty_name(stem)


def build_algo_prompt(group: str, title: str) -> str:
    template = ALGO_PROMPT_BY_GROUP.get(group, ALGO_PROMPT_BY_GROUP["misc"])
    return template.format(title=title)


def is_pure_data_expression(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (str, int, float, bool, complex, type(None)))
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(is_pure_data_expression(element) for element in node.elts)
    if isinstance(node, ast.Dict):
        return all(
            key is None or is_pure_data_expression(key) for key in node.keys
        ) and all(is_pure_data_expression(value) for value in node.values)
    return False


def mutate_string_literal(value: str, variant: int, protected_strings: list[str] | None = None) -> str:
    if not value:
        return f"sample{variant}"

    protected_strings = [item for item in (protected_strings or []) if item]
    if protected_strings and any(item in value for item in protected_strings):
        pattern = re.compile("|".join(re.escape(item) for item in sorted(set(protected_strings), key=len, reverse=True)))
        parts = []
        last = 0
        for match in pattern.finditer(value):
            if match.start() > last:
                parts.append(mutate_string_literal(value[last:match.start()], variant, []))
            parts.append(match.group(0))
            last = match.end()
        if last < len(value):
            parts.append(mutate_string_literal(value[last:], variant, []))
        return "".join(parts)

    shifted = []
    for char in value:
        if "a" <= char <= "z":
            offset = (ord(char) - ord("a") + variant) % 26
            shifted.append(chr(ord("a") + offset))
        elif "A" <= char <= "Z":
            offset = (ord(char) - ord("A") + variant) % 26
            shifted.append(chr(ord("A") + offset))
        elif "0" <= char <= "9":
            offset = (ord(char) - ord("0") + variant) % 10
            shifted.append(chr(ord("0") + offset))
        else:
            shifted.append(char)
    return "".join(shifted)


def collect_protected_literals(reference_code: str) -> tuple[set[object], list[str]]:
    protected_values: set[object] = set()
    protected_strings: list[str] = []
    try:
        module = ast.parse(reference_code)
    except SyntaxError:
        return protected_values, protected_strings

    for node in ast.walk(module):
        if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float, bool)):
            protected_values.add(node.value)
            if isinstance(node.value, str):
                protected_strings.append(node.value)
    return protected_values, protected_strings


def mutate_expression_value(
    node: ast.AST,
    variant: int,
    protected_values: set[object] | None = None,
    protected_strings: list[str] | None = None,
) -> ast.AST:
    node = copy.deepcopy(node)
    protected_values = protected_values or set()
    protected_strings = protected_strings or []

    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, bool):
            if value in protected_values:
                return node
            return ast.copy_location(ast.Constant(value=not value if variant % 2 else value), node)
        if isinstance(value, int):
            if value in protected_values:
                return node
            return ast.copy_location(ast.Constant(value=value + variant), node)
        if isinstance(value, float):
            if value in protected_values:
                return node
            return ast.copy_location(ast.Constant(value=value + float(variant)), node)
        if isinstance(value, str):
            if value in protected_values:
                return node
            return ast.copy_location(ast.Constant(value=mutate_string_literal(value, variant, protected_strings)), node)
        return node

    if isinstance(node, ast.List):
        node.elts = [mutate_expression_value(element, variant, protected_values, protected_strings) for element in node.elts]
        return node
    if isinstance(node, ast.Tuple):
        node.elts = [mutate_expression_value(element, variant, protected_values, protected_strings) for element in node.elts]
        return node
    if isinstance(node, ast.Set):
        node.elts = [mutate_expression_value(element, variant, protected_values, protected_strings) for element in node.elts]
        return node
    if isinstance(node, ast.Dict):
        node.keys = [mutate_expression_value(key, variant, protected_values, protected_strings) if key is not None else None for key in node.keys]
        node.values = [mutate_expression_value(value, variant, protected_values, protected_strings) for value in node.values]
        return node
    if isinstance(node, ast.UnaryOp):
        node.operand = mutate_expression_value(node.operand, variant, protected_values, protected_strings)
        return node
    if isinstance(node, ast.Call):
        node.args = [mutate_expression_value(argument, variant, protected_values, protected_strings) for argument in node.args]
        for keyword in node.keywords:
            keyword.value = mutate_expression_value(keyword.value, variant, protected_values, protected_strings)
        return node
    if isinstance(node, ast.BinOp):
        node.left = mutate_expression_value(node.left, variant, protected_values, protected_strings)
        node.right = mutate_expression_value(node.right, variant, protected_values, protected_strings)
        return node
    return node


def build_variant_input(
    setup_source: str,
    variant: int,
    protected_values: set[object] | None = None,
    protected_strings: list[str] | None = None,
) -> str:
    if not setup_source.strip():
        return f"# No explicit setup required\n# Variant {variant}"

    try:
        module = ast.parse(setup_source)
    except SyntaxError:
        return setup_source if variant == 1 else setup_source + f"\n# Variant {variant}"

    changed = False
    for node in module.body:
        if isinstance(node, ast.Assign):
            node.value = mutate_expression_value(node.value, variant, protected_values, protected_strings)
            changed = True
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            node.value = mutate_expression_value(node.value, variant, protected_values, protected_strings)
            changed = True

    candidate = ast.unparse(module).strip()
    if not candidate:
        return f"# Variant {variant}"
    if candidate == setup_source.strip():
        return candidate + f"\n# Variant {variant}"
    return candidate


def run_solution_test_case(solution_code: str, test_input: str, call_expression: str) -> str:
    parts = [
        '__name__ = "__coding_practice_test__"',
        solution_code.strip(),
    ]
    if test_input.strip():
        parts.append(test_input.strip())
    if call_expression.strip():
        parts.append(call_expression.strip())
    return run_code_capture_output("\n\n".join(parts))


def build_standalone_artifacts(solution_code: str, prompt: str = "") -> tuple[list[dict], list[dict], list[str]]:
    examples: list[dict] = []
    test_cases: list[dict] = []
    notes: list[str] = []
    example_input = summarize_example_input(solution_code, prompt=prompt)

    try:
        example_output = run_code_capture_output(solution_code)
        examples = [{"input": example_input, "output": example_output}]
    except Exception as exc:
        notes.append(f"Example output could not be generated automatically: {exc}")
        return examples, test_cases, notes

    if should_disable_tests(solution_code):
        return examples, test_cases, notes

    try:
        expected_output = run_solution_test_case(solution_code, "", "main()")
        if "__name__" in solution_code and expected_output != example_output:
            notes.append("Automated tests are skipped because runtime module naming changes the output.")
            return examples, test_cases, notes
        test_cases = build_minimum_test_cases("", expected_output, "main()", minimum=1)
    except Exception as exc:
        notes.append(f"Automatic test generation was skipped: {exc}")

    return examples, test_cases, notes


def generate_unique_test_cases(
    solution_code: str,
    setup_source: str,
    call_expression: str,
    reference_code: str = "",
    minimum: int = 3,
) -> list[dict]:
    cases = []
    seen_inputs = set()
    protected_values, protected_strings = collect_protected_literals(reference_code)

    for variant in range(1, minimum + 1):
        candidate_input = (
            setup_source.strip()
            if variant == 1
            else build_variant_input(setup_source, variant, protected_values, protected_strings)
        )
        if candidate_input in seen_inputs:
            candidate_input = (candidate_input + f"\n# Variant {variant}").strip()
        seen_inputs.add(candidate_input)

        try:
            expected_output = run_solution_test_case(solution_code, candidate_input, call_expression)
        except Exception:
            if variant == 1:
                raise
            candidate_input = (setup_source.strip() if setup_source.strip() else "# No explicit setup required") + f"\n# Variant {variant}"
            expected_output = run_solution_test_case(solution_code, candidate_input, call_expression)

        cases.append(
            {
                "input": candidate_input,
                "expected_output": expected_output,
                "call": call_expression,
                "label": f"Test {variant}",
            }
        )

    return cases


def run_code_capture_output(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as handle:
        handle.write(code)
        temp_path = Path(handle.name)

    try:
        result = subprocess.run(
            [sys.executable, str(temp_path)],
            capture_output=True,
            text=True,
            timeout=5,
        )
    finally:
        temp_path.unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Execution failed")
    return result.stdout.strip()


def should_disable_tests(code: str) -> bool:
    unstable_markers = (
        "input(",
        "sys.argv",
        "time.time(",
        "random.",
        "open(",
    )
    return any(marker in code for marker in unstable_markers)


def safe_example_input(value: str) -> str:
    cleaned = value.strip()
    return cleaned or "No explicit input setup required."


def build_problem_id(category_id: str, sequence: int, title: str) -> str:
    return f"{category_id}_{sequence:02d}_{slugify(title)[:60]}"


def build_storage_problem(
    category: dict,
    problem: ProblemRecord,
) -> dict:
    problem_id = build_problem_id(category["id"], problem.sequence, problem.title)
    storage_problem = {
        "id": problem_id,
        "sequence": problem.sequence,
        "category_id": category["id"],
        "category_name": category["name"],
        "title": problem.title,
        "description": build_description(problem.prompt, problem.notes, bool(problem.test_cases)),
        "prompt": problem.prompt,
        "difficulty": problem.difficulty,
        "starter_code": problem.starter_code,
        "solution": problem.solution,
        "examples": problem.examples,
        "test_cases": problem.test_cases,
        "notes": filter_user_notes(problem.notes),
        "source_reference": problem.source_reference,
    }
    return storage_problem


def extract_question_titles_from_comments(source: str) -> list[str]:
    matches = re.findall(r'#\s*print\("(.+?) - Question \d+"\)', source)
    return matches


def parse_questions_assignment(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    module_import_lines = [
        node_to_source(node)
        for node in module.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "scripts.common")
    ]
    question_list = None
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "questions":
                    question_list = ast.literal_eval(node.value)
                    break
    if not question_list:
        return []

    titles = extract_question_titles_from_comments(source)
    problems = []
    for index, question in enumerate(question_list, start=1):
        title = titles[index - 1] if index - 1 < len(titles) else f"Question {index}"
        notes: list[str] = []
        prompt = question["question"].split("Expected output:")[0].strip().rstrip(".") + "."
        setup_code = question.get("input_code", "").strip()
        support_source, input_source = split_support_and_input_setup(setup_code)
        action_code = question.get("test_case", "").strip()
        if not input_source.strip():
            derived_input_source, transformed_action = parameterize_action_source(action_code, support_source)
            if derived_input_source.strip():
                input_source = derived_input_source
                action_code = transformed_action
        import_lines = dedupe_preserve_order(module_import_lines + import_lines_from_source(setup_code + "\n" + action_code))
        parameter_names = extract_parameter_names_from_setup(input_source)
        call_expression = build_call_expression(parameter_names)
        starter_code = build_wrapped_code(
            import_lines,
            support_source=support_source,
            setup_source=input_source,
            parameter_names=parameter_names,
            placeholder=True,
        )
        solution = build_wrapped_code(
            import_lines,
            support_source=support_source,
            setup_source=input_source,
            main_body=action_code,
            parameter_names=parameter_names,
        )
        try:
            test_cases = generate_unique_test_cases(solution, input_source, call_expression)
            examples = [
                {
                    "input": safe_example_input(test_cases[0]["input"]),
                    "output": test_cases[0]["expected_output"],
                }
            ]
        except Exception as exc:
            test_cases = []
            examples = []
            notes.append(f"Automatic test generation was skipped: {exc}")
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=index,
                starter_code=starter_code,
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": index},
            )
        )
    return problems


def is_question_block_start(text: str | None) -> bool:
    if not text:
        return False
    stripped = text.strip()
    return bool(
        re.match(r".+\s*-\s*Question \d+$", stripped)
        or re.match(r"Question \d+: .+", stripped)
        or re.match(r"-{3}\s*Question \d+\s*-{3}", stripped)
    )


def parse_title_and_sequence(text: str, fallback_sequence: int) -> tuple[str, int]:
    stripped = text.strip()
    match = re.match(r"(.+?)\s*-\s*Question (\d+)$", stripped)
    if match:
        return match.group(1).strip(), int(match.group(2))
    match = re.match(r"Question (\d+): (.+)$", stripped)
    if match:
        return match.group(2).strip(), int(match.group(1))
    match = re.match(r"-{3}\s*Question (\d+)\s*-{3}", stripped)
    if match:
        return f"Question {match.group(1)}", int(match.group(1))
    return stripped or f"Question {fallback_sequence}", fallback_sequence


def collect_print_blocks(module: ast.Module) -> list[list[ast.AST]]:
    blocks = []
    current: list[ast.AST] = []
    for node in module.body:
        text = first_print_text(node)
        if is_question_block_start(text):
            if current:
                blocks.append(current)
            current = [node]
        elif current:
            current.append(node)
    if current:
        blocks.append(current)
    return blocks


def normalize_statement(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=False, include_attributes=False)


def parse_code_statements(code_lines: list[str]) -> list[ast.AST]:
    combined = normalize_code_block("\n".join(line for line in code_lines if line.strip()))
    if not combined:
        return []
    return ast.parse(combined).body


def normalize_code_block(code: str) -> str:
    normalized = textwrap.dedent(code).strip()
    if not normalized:
        return ""

    try:
        ast.parse(normalized)
        return normalized
    except SyntaxError as exc:
        if "unexpected indent" not in str(exc):
            return normalized

    lines = normalized.splitlines()
    for _ in range(8):
        if len(lines) < 2:
            break
        lines = [lines[0]] + [
            line[1:] if line[:1] in {" ", "\t"} else line
            for line in lines[1:]
        ]
        candidate = "\n".join(lines).strip()
        try:
            ast.parse(candidate)
            return candidate
        except SyntaxError:
            continue

    return normalized


def defined_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        names.add(node.name)
    elif isinstance(node, ast.Import):
        for alias in node.names:
            names.add(alias.asname or alias.name.split(".")[0])
    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            names.add(alias.asname or alias.name)
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            names.update(extract_target_names(target))
    elif isinstance(node, ast.AnnAssign):
        names.update(extract_target_names(node.target))
    elif isinstance(node, ast.AugAssign):
        names.update(extract_target_names(node.target))
    return names


def extract_target_names(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, (ast.Tuple, ast.List)):
        names: set[str] = set()
        for element in node.elts:
            names.update(extract_target_names(element))
        return names
    return set()


def mutated_names(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Delete):
        names: set[str] = set()
        for target in node.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                names.add(target.value.id)
            else:
                names.update(extract_target_names(target))
        return names

    if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
        return set()

    func = node.value.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return {func.value.id}
    return set()


def loaded_names(nodes: Iterable[ast.AST]) -> set[str]:
    names: set[str] = set()
    for node in nodes:
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                names.add(child.id)
    return names


def context_nodes_from_block(block: list[ast.AST]) -> list[ast.AST]:
    context_nodes = []
    for node in block:
        if is_print_call(node):
            continue
        if isinstance(
            node,
            (
                ast.Import,
                ast.ImportFrom,
                ast.Assign,
                ast.AnnAssign,
                ast.AugAssign,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
                ast.Delete,
            ),
        ):
            context_nodes.append(node)
        elif mutated_names(node):
            context_nodes.append(node)
    return context_nodes


def executable_nodes_from_block(block: list[ast.AST]) -> list[ast.AST]:
    return [node for node in block if not is_print_call(node)]


def derived_output_statements(source: str, block: list[ast.AST]) -> tuple[list[str], list[ast.AST]]:
    statements = []
    fallback_statements = []
    output_nodes: list[ast.AST] = []
    seen_action = False
    for node in block:
        if not is_print_call(node):
            if isinstance(
                node,
                (
                    ast.Assign,
                    ast.AnnAssign,
                    ast.AugAssign,
                    ast.Expr,
                    ast.Delete,
                    ast.For,
                    ast.While,
                    ast.If,
                    ast.Try,
                ),
            ):
                seen_action = True
            continue
        segment = ast.get_source_segment(source, node)
        text = first_print_text(node)
        if not text:
            if seen_action and segment and ('Output' in segment or 'Answer' in segment):
                statements.append(segment.strip())
            continue
        stripped = text.strip()
        if (
            is_question_block_start(text)
            or stripped.startswith(("Question:", "Description:", "Input:", "Code:"))
            or stripped == "-" * 20
        ):
            continue
        call = node.value
        extra_args = call.args[1:]
        if stripped.startswith(("Output", "Answer")):
            if extra_args:
                statements.append(f"print({', '.join(ast.unparse(arg) for arg in extra_args)})")
                output_nodes.extend(extra_args)
            elif segment:
                statements.append(segment.strip())
            continue
        if seen_action and segment:
            fallback_statements.append(segment.strip())
    return (statements or fallback_statements), output_nodes


def fallback_block_source(source: str, block: list[ast.AST]) -> str:
    kept_segments = []
    for node in block:
        text = first_print_text(node)
        if text:
            stripped = text.strip()
            if (
                is_question_block_start(text)
                or stripped.startswith(("Question:", "Description:", "Input:", "Code:"))
                or stripped == "-" * 20
            ):
                continue
        segment = ast.get_source_segment(source, node)
        if segment:
            kept_segments.append(segment.strip())
    return "\n\n".join(segment for segment in kept_segments if segment).strip()


def find_action_start(state_nodes: list[ast.AST], code_nodes: list[ast.AST]) -> int:
    if not code_nodes:
        return 0
    needle = [normalize_statement(node) for node in code_nodes]
    haystack = [normalize_statement(node) for node in state_nodes]
    for index in range(len(haystack) - len(needle) + 1):
        if haystack[index : index + len(needle)] == needle:
            return index
    for index, statement in enumerate(haystack):
        if statement == needle[0]:
            return index
    return len(state_nodes)


def build_minimal_setup(history: list[ast.AST], prefix_nodes: list[ast.AST], action_nodes: list[ast.AST], extra_output_nodes: list[ast.AST]) -> list[ast.AST]:
    search_nodes = history + prefix_nodes
    needed = loaded_names(action_nodes + extra_output_nodes) - defined_names_from_nodes(action_nodes)
    needed -= BUILTIN_NAMES
    chosen: list[ast.AST] = []
    for node in reversed(search_nodes):
        defs = defined_names(node)
        muts = mutated_names(node)
        if not (defs & needed or muts & needed):
            continue
        chosen.append(node)
        needed.update(loaded_names([node]) - BUILTIN_NAMES)
        needed -= defs
    chosen.reverse()
    return chosen


def defined_names_from_nodes(nodes: Iterable[ast.AST]) -> set[str]:
    names: set[str] = set()
    for node in nodes:
        names.update(defined_names(node))
    return names


def collect_callable_signatures(*sources: str) -> dict[str, dict[str, object]]:
    signatures: dict[str, dict[str, object]] = {}
    for source in sources:
        if not source.strip():
            continue
        try:
            module = ast.parse(source)
        except SyntaxError:
            continue

        for node in module.body:
            if isinstance(node, ast.FunctionDef):
                signatures[node.name] = {
                    "positional": [arg.arg for arg in node.args.args],
                    "vararg": node.args.vararg.arg if node.args.vararg else None,
                    "kwarg": node.args.kwarg.arg if node.args.kwarg else None,
                }
            elif (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Lambda)
            ):
                signatures[node.targets[0].id] = {
                    "positional": [arg.arg for arg in node.value.args.args],
                    "vararg": node.value.args.vararg.arg if node.value.args.vararg else None,
                    "kwarg": node.value.args.kwarg.arg if node.value.args.kwarg else None,
                }
    return signatures


def parameterize_action_source(action_source: str, support_source: str = "") -> tuple[str, str]:
    if not action_source.strip():
        return "", action_source.strip()

    try:
        module = ast.parse(action_source)
    except SyntaxError:
        return "", action_source.strip()

    signatures = collect_callable_signatures(support_source, action_source)
    reserved_names = BUILTIN_NAMES | defined_names_from_nodes(module.body)
    created_names: set[str] = set()
    input_assignments: list[str] = []
    input_counter = 0

    def unique_name(name_hint: str) -> str:
        base = slugify(name_hint).replace("-", "_") or "input"
        candidate = base
        suffix = 2
        while candidate in reserved_names or candidate in created_names:
            candidate = f"{base}_{suffix}"
            suffix += 1
        created_names.add(candidate)
        return candidate

    def register_input(name_hint: str, expression: ast.AST) -> ast.Name:
        nonlocal input_counter
        input_counter += 1
        preferred = name_hint or f"input_{input_counter}"
        input_name = unique_name(preferred)
        input_assignments.append(f"{input_name} = {ast.unparse(expression).strip()}")
        return ast.copy_location(ast.Name(id=input_name, ctx=ast.Load()), expression)

    class LiteralInputTransformer(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
            return node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
            return node

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
            return node

        def visit_Lambda(self, node: ast.Lambda) -> ast.AST:
            return node

        def visit_JoinedStr(self, node: ast.JoinedStr) -> ast.AST:
            return node

        def visit_Call(self, node: ast.Call) -> ast.AST:
            node.func = self.visit(node.func)
            signature = node.func.id if isinstance(node.func, ast.Name) else None
            signature_data = signatures.get(signature or "")

            new_args = []
            for index, argument in enumerate(node.args, start=1):
                if is_pure_data_expression(argument):
                    if signature_data and index <= len(signature_data["positional"]):
                        hint = signature_data["positional"][index - 1]
                    elif signature_data and signature_data.get("vararg"):
                        hint = f"{signature_data['vararg']}_{index}"
                    else:
                        hint = f"input_{input_counter + 1}"
                    new_args.append(register_input(hint, argument))
                else:
                    new_args.append(self.visit(argument))
            node.args = new_args

            new_keywords = []
            for keyword in node.keywords:
                if keyword.arg and is_pure_data_expression(keyword.value):
                    keyword.value = register_input(keyword.arg, keyword.value)
                else:
                    keyword.value = self.visit(keyword.value)
                new_keywords.append(keyword)
            node.keywords = new_keywords
            return node

        def visit_List(self, node: ast.List) -> ast.AST:
            if is_pure_data_expression(node):
                return register_input("items", node)
            return self.generic_visit(node)

        def visit_Tuple(self, node: ast.Tuple) -> ast.AST:
            if is_pure_data_expression(node):
                return register_input("items", node)
            return self.generic_visit(node)

        def visit_Set(self, node: ast.Set) -> ast.AST:
            if is_pure_data_expression(node):
                return register_input("items", node)
            return self.generic_visit(node)

        def visit_Dict(self, node: ast.Dict) -> ast.AST:
            if is_pure_data_expression(node):
                return register_input("mapping", node)
            return self.generic_visit(node)

        def visit_Constant(self, node: ast.Constant) -> ast.AST:
            if isinstance(node.value, (str, int, float, bool, complex, type(None))):
                return register_input("value", node)
            return node

    transformer = LiteralInputTransformer()
    transformed_body: list[ast.AST] = []
    for statement in module.body:
        if (
            isinstance(statement, ast.Assign)
            and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
            and is_pure_data_expression(statement.value)
        ):
            target_name = statement.targets[0].id
            created_names.add(target_name)
            input_assignments.append(f"{target_name} = {ast.unparse(statement.value).strip()}")
            continue
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.value is not None
            and is_pure_data_expression(statement.value)
        ):
            target_name = statement.target.id
            created_names.add(target_name)
            input_assignments.append(f"{target_name} = {ast.unparse(statement.value).strip()}")
            continue
        transformed_body.append(transformer.visit(copy.deepcopy(statement)))

    transformed_module = ast.Module(body=transformed_body, type_ignores=[])
    ast.fix_missing_locations(transformed_module)
    transformed_action = ast.unparse(transformed_module).strip()
    input_source = "\n\n".join(input_assignments).strip()

    if not input_source:
        return "", action_source.strip()
    return input_source, transformed_action


def parse_standard_question_file(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    module_import_lines = [
        node_to_source(node)
        for node in module.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "scripts.common")
    ]
    blocks = collect_print_blocks(module)
    history_context: list[ast.AST] = []
    problems: list[ProblemRecord] = []

    for fallback_sequence, block in enumerate(blocks, start=1):
        title, sequence = parse_title_and_sequence(first_print_text(block[0]) or "", fallback_sequence)
        prompt = ""
        notes: list[str] = []
        code_lines: list[str] = []
        example_input = ""

        for node in block[1:]:
            text = first_print_text(node)
            if not text:
                continue
            stripped = text.strip()
            if stripped.startswith("Question:"):
                prompt = stripped.split("Question:", 1)[1].strip()
            elif stripped.startswith("Description:"):
                notes.append(stripped.split("Description:", 1)[1].strip())
            elif stripped.startswith("Input:"):
                example_input = text.split("Input:", 1)[1].strip()
            elif stripped.startswith("Code:"):
                code_lines.append(text.split("Code:", 1)[1].strip())
            elif "Expected output:" in stripped and not prompt:
                prompt = stripped
            elif stripped and stripped not in {"-" * 20} and not stripped.startswith("Output"):
                notes.append(stripped)

        state_nodes = context_nodes_from_block(block)
        all_exec_nodes = executable_nodes_from_block(block)
        output_lines, output_expr_nodes = derived_output_statements(source, block)
        block_fallback_mode = False

        try:
            code_nodes = parse_code_statements(code_lines)
        except SyntaxError:
            code_nodes = []
            block_fallback_mode = True

        action_start = find_action_start(state_nodes, code_nodes)
        prefix_nodes = state_nodes[:action_start]

        if block_fallback_mode:
            action_source = fallback_block_source(source, block)
        elif code_lines:
            action_source = normalize_code_block("\n".join(code_lines))
            if output_lines and "print(" not in action_source:
                action_source = action_source + "\n" + "\n".join(output_lines)
            fallback_source = fallback_block_source(source, block)
            if fallback_source and should_disable_tests(fallback_source):
                action_source = fallback_block_source(source, block)
                block_fallback_mode = True
        else:
            action_nodes = all_exec_nodes[action_start:] if all_exec_nodes else []
            action_source = nodes_to_source(action_nodes).strip()

        if not action_source:
            history_context.extend(state_nodes)
            continue

        try:
            action_nodes = ast.parse(action_source).body
        except SyntaxError:
            action_nodes = []
            block_fallback_mode = True

        if block_fallback_mode:
            setup_source = ""
            test_cases = []
            examples = []
            notes.append("Stored as a standalone snippet because the block is not a simple hidden-setup exercise.")
        else:
            setup_nodes = build_minimal_setup(history_context, prefix_nodes, action_nodes, output_expr_nodes)
            setup_source = nodes_to_source(setup_nodes).strip()
            support_source, input_source = split_support_and_input_setup(setup_source)
            test_cases = []
            if not should_disable_tests("\n\n".join(part for part in (setup_source, action_source) if part.strip())):
                try:
                    setup_input = input_source
                    if not example_input:
                        example_input = safe_example_input(setup_source)
                    examples = []
                except Exception as exc:
                    notes.append(f"Expected output could not be generated automatically: {exc}")
                    examples = []
            else:
                examples = []

        solution_parts = [part for part in (setup_source, action_source) if part.strip()]
        if not prompt:
            prompt = title

        if block_fallback_mode:
            import_lines, fallback_body = split_imports_and_body(action_source)
            starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
            solution = build_wrapped_code(import_lines, main_body=fallback_body)
            examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
            notes.extend(extra_notes)
        else:
            support_source, input_source = split_support_and_input_setup(setup_source)
            if not input_source.strip():
                derived_input_source, transformed_action = parameterize_action_source(action_source, support_source)
                if derived_input_source.strip():
                    input_source = derived_input_source
                    action_source = transformed_action
            parameter_names = extract_parameter_names_from_setup(input_source)
            call_expression = build_call_expression(parameter_names)
            import_lines = dedupe_preserve_order(module_import_lines + import_lines_from_source(setup_source + "\n" + action_source))
            starter_code = build_wrapped_code(
                import_lines,
                support_source=support_source,
                setup_source=input_source,
                parameter_names=parameter_names,
                placeholder=True,
            )
            solution = build_wrapped_code(
                import_lines,
                support_source=support_source,
                setup_source=input_source,
                main_body=action_source,
                parameter_names=parameter_names,
            )
            if not should_disable_tests(solution):
                try:
                    test_cases = generate_unique_test_cases(solution, input_source, call_expression)
                    examples = [{"input": safe_example_input(test_cases[0]["input"]), "output": test_cases[0]["expected_output"]}]
                except Exception as exc:
                    notes.append(f"Automatic test generation was skipped: {exc}")
                    test_cases = []
                    examples = []
            elif not examples:
                examples, _, extra_notes = build_standalone_artifacts(solution, prompt)
                notes.extend(extra_notes)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
        history_context.extend(state_nodes)

    return problems


def parse_operator_precedence(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    blocks = collect_print_blocks(module)
    problems = []

    for fallback_sequence, block in enumerate(blocks, start=1):
        question_expression = ""
        description = ""
        answer_expression = ""
        _, sequence = parse_title_and_sequence(first_print_text(block[0]) or "", fallback_sequence)

        for node in block[1:]:
            text = first_print_text(node)
            if text and text.strip().startswith("Question:"):
                question_expression = text.split("Question:", 1)[1].strip()
            elif text and text.strip().startswith("Description:"):
                description = text.split("Description:", 1)[1].strip()
            elif is_print_call(node):
                call = node.value
                first = first_print_text(node)
                if first and first.strip().startswith("Answer:") and len(call.args) > 1:
                    answer_expression = ast.unparse(call.args[1]).strip()

        if not question_expression:
            continue

        title = question_expression
        prompt = description or f"Evaluate this expression using Python operator precedence: {question_expression}"
        action_code = f"print({answer_expression or question_expression})"
        input_source, transformed_action = parameterize_action_source(action_code)
        parameter_names = extract_parameter_names_from_setup(input_source)
        call_expression = build_call_expression(parameter_names)
        starter_code = build_wrapped_code([], setup_source=input_source, parameter_names=parameter_names, placeholder=True)
        solution = build_wrapped_code([], setup_source=input_source, main_body=transformed_action, parameter_names=parameter_names)
        test_cases = generate_unique_test_cases(solution, input_source, call_expression)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=solution,
                test_cases=test_cases,
                examples=[{"input": safe_example_input(test_cases[0]["input"]), "output": test_cases[0]["expected_output"]}],
                source_reference={"file": path.name, "question": sequence},
            )
        )
    return problems


def parse_arrays_file(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    module_imports = [
        node_to_source(node)
        for node in module.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "scripts.common")
    ]
    problems = []
    sequence = 1
    for node in module.body:
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("question_"):
            continue

        title = pretty_name(node.name.replace("question_", ""))
        prompt = title + "."
        body_nodes = []
        for child in node.body:
            text = first_print_text(child)
            if text and text.strip().startswith("Question:"):
                prompt = text.split("Question:", 1)[1].strip()
                continue
            if is_print_function_call(child):
                continue
            body_nodes.append(child)

        action_source = "\n\n".join(
            part for part in ("\n".join(module_imports), nodes_to_source(body_nodes)) if part.strip()
        ).strip()
        import_lines, action_body = split_imports_and_body(action_source)
        starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
        solution = build_wrapped_code(import_lines, main_body=action_body)
        examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
        notes = ["This problem is stored as a runnable standalone snippet."]
        notes.extend(extra_notes)

        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
        sequence += 1
    return problems


def parse_demo_functions(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    imports = [
        node_to_source(node)
        for node in module.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "scripts.common")
    ]
    function_map = {node.name: node for node in module.body if isinstance(node, ast.FunctionDef)}
    call_order = []
    for node in module.body:
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id in function_map
        ):
            call_order.append(node.value.func.id)

    problems = []
    for sequence, function_name in enumerate(call_order, start=1):
        function_node = function_map[function_name]
        title = pretty_name(function_name)
        prompt = title + "."
        for child in function_node.body:
            text = first_print_text(child)
            if text:
                cleaned = text.strip().strip("-").strip()
                if cleaned:
                    prompt = cleaned if cleaned.endswith(".") else cleaned + "."
                    break
        prompt = override_prompt(
            path,
            title,
            f"{prompt.rstrip('.')} Use the sample setup shown below and match the example output.",
        )

        filtered_body = [child for child in function_node.body if not is_print_function_call(child)]
        function_clone = ast.FunctionDef(
            name=function_node.name,
            args=function_node.args,
            body=filtered_body or [ast.Pass()],
            decorator_list=function_node.decorator_list,
            returns=function_node.returns,
            type_comment=function_node.type_comment,
        )
        ast.fix_missing_locations(function_clone)
        action_parts = imports + [node_to_source(function_clone), f"{function_name}()"]
        action_source = "\n\n".join(part for part in action_parts if part.strip())
        import_lines, action_body = split_imports_and_body(action_source)
        starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
        notes: list[str] = []
        if "input(" in action_source or "sys.argv" in action_source:
            notes.append("Tests are disabled because this example expects live user input or command-line arguments.")
        solution = build_wrapped_code(import_lines, main_body=action_body)
        examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
        notes.extend(extra_notes)

        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
    return problems


def parse_heading_sections(path: Path, source: str) -> list[ProblemRecord]:
    lines = source.splitlines()
    blocks: list[list[str]] = []
    current: list[str] = []

    def is_heading(line: str) -> bool:
        stripped = line.strip()
        if stripped.startswith('print("\\n---') or stripped.startswith('print("\\nConcept'):
            return True
        if stripped.startswith('print("Additional Information'):
            return True
        return False

    for line in lines:
        if is_heading(line):
            if current:
                blocks.append(current)
            current = [line]
        elif current:
            current.append(line)
    if current:
        blocks.append(current)

    problems = []
    for sequence, block_lines in enumerate(blocks, start=1):
        heading_line = block_lines[0].strip()
        heading_match = re.search(r'print\("([^"]+)"\)', heading_line)
        title = pretty_name((heading_match.group(1) if heading_match else f"Section {sequence}").replace("---", " "))
        prompt = override_prompt(
            path,
            title,
            f'Recreate the "{title}" demonstration inside main() using the sample values shown below, and print the same labeled output as the example.',
        )
        action_source = "\n".join(block_lines).strip() + "\n"
        import_lines, action_body = split_imports_and_body(action_source)
        starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
        solution = build_wrapped_code(import_lines, main_body=action_body)
        examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
        notes = list(extra_notes)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
    return problems


def parse_bitwise(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    imports = [
        node_to_source(node)
        for node in module.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        and not (isinstance(node, ast.ImportFrom) and node.module == "scripts.common")
    ]
    problems = []
    sequence = 1

    for node in module.body:
        if not isinstance(node, ast.FunctionDef):
            continue

        body = node.body
        index = 0
        while index < len(body):
            current = body[index]
            if isinstance(current, ast.FunctionDef):
                nested_function = current
                title = pretty_name(nested_function.name)
                prompt = title + "."
                call_expression = ""
                scan_index = index + 1
                while scan_index < len(body):
                    scan_node = body[scan_index]
                    text = first_print_text(scan_node)
                    if text and text.strip().startswith("Question:"):
                        prompt = text.split("Question:", 1)[1].strip()
                    if is_print_call(scan_node):
                        call = scan_node.value
                        label = first_print_text(scan_node)
                        if label and label.strip().startswith("Output:") and len(call.args) > 1:
                            call_expression = f"print({ast.unparse(call.args[1])})"
                            break
                    if isinstance(scan_node, ast.FunctionDef):
                        break
                    scan_index += 1

                action_parts = imports + [node_to_source(nested_function)]
                if call_expression:
                    action_parts.append(call_expression)
                action_source = "\n\n".join(part for part in action_parts if part.strip()) + "\n"
                import_lines, action_body = split_imports_and_body(action_source)
                starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
                solution = build_wrapped_code(import_lines, main_body=action_body)
                examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
                notes = list(extra_notes)
                problems.append(
                    ProblemRecord(
                        title=pretty_name(prompt.split(".")[0]),
                        prompt=prompt,
                        sequence=sequence,
                        starter_code=starter_code,
                        solution=solution,
                        test_cases=test_cases,
                        examples=examples,
                        notes=notes,
                        source_reference={"file": path.name, "question": sequence},
                    )
                )
                sequence += 1
            index += 1

    return problems


def parse_underscore_and_dunder(path: Path, source: str) -> list[ProblemRecord]:
    module = ast.parse(source)
    wrapper_map = {
        node.name: node for node in module.body if isinstance(node, ast.FunctionDef) and node.name.startswith("wrapper_")
    }
    title_map = {
        "wrapper_single_underscore_for_internal": "Single Underscore for Internal Use",
        "wrapper_single_underscore_for_ignore": "Single Underscore as an Ignored Variable",
        "wrapper_double_underscore_for_avoiding_conflicts": "Double Underscore Name Mangling",
        "wrapper_double_underscore_for_special_methods": "Dunder Special Methods",
    }

    problems = []
    sequence = 1
    for name, node in wrapper_map.items():
        action_source = node_to_source(node) + f"\n\n{name}()\n"
        solution = build_wrapped_code([], main_body=action_source.strip())
        title = title_map.get(name, pretty_name(name))
        prompt = override_prompt(
            path,
            title,
            f"Recreate the {title.lower()} example inside main() using the sample setup shown below, and match the example output.",
        )
        examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
        notes = list(extra_notes)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=build_wrapped_code([], parameter_names=[], placeholder=True),
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
        sequence += 1

    solution = build_wrapped_code([], main_body="print(__name__)")
    module_name_prompt = override_prompt(path, "Module __name__ Value", "Print the module __name__ value.")
    examples, test_cases, extra_notes = build_standalone_artifacts(solution, module_name_prompt)
    notes = list(extra_notes)
    problems.append(
        ProblemRecord(
            title="Module __name__ Value",
            prompt=module_name_prompt,
            sequence=sequence,
            starter_code=build_wrapped_code([], parameter_names=[], placeholder=True),
            solution=solution,
            test_cases=test_cases,
            examples=examples,
            notes=notes,
            source_reference={"file": path.name, "question": sequence},
        )
    )
    return problems


def parse_inheritance_types(path: Path, source: str) -> list[ProblemRecord]:
    markers = [
        ("##Single", "Single Inheritance"),
        ("##Multilevel", "Multilevel Inheritance"),
        ("### Multiple", "Multiple Inheritance"),
    ]
    prompt_map = {
        "Single Inheritance": (
            "Create an Animal class with a speak() method and a Dog class that inherits from Animal "
            "and adds a bark() method. Inside main(), instantiate Dog and call speak() first, then bark()."
        ),
        "Multilevel Inheritance": (
            "Create an Animal class with speak(), a Dog class that inherits from Animal with bark(), "
            "and a Puppy class that inherits from Dog with weep(). Inside main(), instantiate Puppy and "
            "call speak(), bark(), and weep() in that order."
        ),
        "Multiple Inheritance": (
            "Create a Father class with height(), a Mother class with intelligence(), and a Child class "
            "that inherits from both. Inside main(), instantiate Child and call height() first, then intelligence()."
        ),
    }
    example_input_map = {
        "Single Inheritance": "Define Animal.speak() and Dog.bark(), then run:\nbuddy = Dog()\nbuddy.speak()\nbuddy.bark()",
        "Multilevel Inheritance": "Define Animal.speak(), Dog.bark(), and Puppy.weep(), then run:\ntiny = Puppy()\ntiny.speak()\ntiny.bark()\ntiny.weep()",
        "Multiple Inheritance": "Define Father.height() and Mother.intelligence(), inherit both in Child, then run:\nchild = Child()\nchild.height()\nchild.intelligence()",
    }
    problems = []
    for sequence, (marker, title) in enumerate(markers, start=1):
        start = source.find(marker)
        if start == -1:
            continue
        next_positions = [source.find(other_marker, start + len(marker)) for other_marker, _ in markers]
        next_positions = [position for position in next_positions if position != -1]
        end = min(next_positions) if next_positions else len(source)
        snippet = source[start:end]
        cleaned = "\n".join(line for line in snippet.splitlines() if not line.strip().startswith("#"))
        import_lines, action_body = split_imports_and_body(cleaned)
        solution = build_wrapped_code(import_lines, main_body=action_body)
        examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt_map[title])
        if examples:
            examples[0]["input"] = example_input_map[title]
        notes = [note for note in extra_notes if not note.startswith("Stored as ")]
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt_map[title],
                sequence=sequence,
                starter_code=build_wrapped_code(import_lines, parameter_names=[], placeholder=True),
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
    return problems


def parse_polymorphism(path: Path, source: str) -> list[ProblemRecord]:
    section_markers = [
        ("Imagine a function that needs to save data.", "Save Data with Duck Typing"),
        ("2) Flexibility:", "Compose with Any Writer"),
        ("3) Runtime Type Checking:", "Runtime Type Checking with hasattr"),
        ("4) Error Potential:", "Error Potential When Methods Are Missing"),
        ("5) hasattr() and getattr():", "hasattr and getattr in Practice"),
    ]
    problems = []
    for sequence, (marker, title) in enumerate(section_markers, start=1):
        start = source.find(marker)
        if start == -1:
            continue
        next_positions = [source.find(other_marker, start + len(marker)) for other_marker, _ in section_markers]
        next_positions = [position for position in next_positions if position != -1]
        end = min(next_positions) if next_positions else len(source)
        snippet = source[start:end]
        code_start = snippet.find("class ")
        if code_start == -1:
            continue
        action_source = snippet[code_start:]
        trailing_docstring = action_source.find('\n"""')
        if trailing_docstring != -1:
            action_source = action_source[:trailing_docstring]
        action_source = action_source.strip() + "\n"
        if title == "Save Data with Duck Typing":
            action_source = action_source.replace(
                "with open('data.txt', 'w') as file:\n            file.write(data)",
                "print(f'Saved to file: {data}')",
            )
        if title == "Error Potential When Methods Are Missing":
            action_source = re.sub(
                r"^(\s*)start_trip\(bicycle\).*$",
                "\\1try:\n\\1    start_trip(bicycle)\n\\1except AttributeError as error:\n\\1    print(f\"AttributeError: {error}\")",
                action_source,
                flags=re.MULTILINE,
            )
        prompt = override_prompt(
            path,
            title,
            f"Recreate the {title.lower()} example inside main() using the sample setup shown below, and match the example output.",
        )
        import_lines, action_body = split_imports_and_body(action_source)
        solution = build_wrapped_code(import_lines, main_body=action_body)
        examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
        notes = list(extra_notes)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=build_wrapped_code(import_lines, parameter_names=[], placeholder=True),
                solution=solution,
                test_cases=test_cases,
                examples=examples,
                notes=notes,
                source_reference={"file": path.name, "question": sequence},
            )
        )
    return problems


def parse_single_snippet(path: Path, source: str) -> list[ProblemRecord]:
    title = TITLE_FROM_FILENAME_MAP.get(path.name, CATEGORY_NAME_MAP.get(path.name, pretty_name(path.stem)))
    prompt = override_prompt(
        path,
        title,
        f"Recreate the {title.lower()} example inside main() using the same structure and sample values shown below, and match the example output.",
    )
    import_lines, action_body = split_imports_and_body(source)
    starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
    solution = build_wrapped_code(import_lines, main_body=action_body)
    examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)
    notes = list(extra_notes)
    return [
        ProblemRecord(
            title=title,
            prompt=prompt,
            sequence=1,
            starter_code=starter_code,
            solution=solution,
            test_cases=test_cases,
            examples=examples,
            notes=notes,
            source_reference={"file": path.name, "question": 1},
        )
    ]


def parse_algo_problem_file(path: Path) -> tuple[str, int, ProblemRecord]:
    """Convert a single algorithm reference file into one runnable problem."""
    raw_source = path.read_text()
    source = normalize_algo_source(path, raw_source)
    group, order, title = algo_file_meta(path)
    prompt = build_algo_prompt(group, title)
    import_lines, support_source, action_body = split_runnable_script(source)
    starter_code = build_wrapped_code(
        import_lines,
        support_source=support_source,
        parameter_names=[],
        placeholder=True,
    )
    solution = build_wrapped_code(
        import_lines,
        support_source=support_source,
        main_body=action_body,
    )
    examples, test_cases, extra_notes = build_standalone_artifacts(solution, prompt)

    problem = ProblemRecord(
        title=title,
        prompt=prompt,
        sequence=0,
        starter_code=starter_code,
        solution=solution,
        test_cases=test_cases,
        examples=examples,
        notes=list(extra_notes),
        source_reference={"file": path.name, "question": 1},
    )
    return group, order, problem


def parse_category_file(path: Path) -> list[ProblemRecord]:
    source = path.read_text()
    extractor_map = {
        "01_strings.py": parse_questions_assignment,
        "02_list.py": parse_standard_question_file,
        "03_tuple.py": parse_standard_question_file,
        "04_set.py": parse_standard_question_file,
        "05_dictionary.py": parse_standard_question_file,
        "06_variables.py": parse_heading_sections,
        "07_datatypes.py": parse_heading_sections,
        "08_operators.py": parse_heading_sections,
        "09_operators-precedence.py": parse_operator_precedence,
        "10_numbersystem-conversion.py": parse_heading_sections,
        "11_bitwise.py": parse_bitwise,
        "12_user-input.py": parse_demo_functions,
        "13_loop-breakers.py": parse_demo_functions,
        "14_arrays.py": parse_arrays_file,
        "15_numpy-1.py": parse_standard_question_file,
        "16_numpy-2.py": parse_standard_question_file,
        "17_numpy_matrix.py": parse_standard_question_file,
        "18_functions-argument-types.py": parse_standard_question_file,
        "19_function-global-keyword.py": parse_standard_question_file,
        "20_functions-mutable-immutable.py": parse_demo_functions,
        "21_lambda.py": parse_standard_question_file,
        "22_decorator.py": parse_single_snippet,
        "23_underscore-and-dunder.py": parse_underscore_and_dunder,
        "24_special_variable_name.py": parse_single_snippet,
        "25_methodtypes.py": parse_single_snippet,
        "26_innerclass.py": parse_single_snippet,
        "27_inheritance_types.py": parse_inheritance_types,
        "28_inheritance_order.py": parse_single_snippet,
        "29_polymorphism-ducktyping.py": parse_polymorphism,
    }

    extractor = extractor_map.get(path.name, parse_single_snippet)
    try:
        problems = extractor(path, source)
        if problems:
            return problems
    except Exception as exc:
        print(f"Warning: failed to parse {path.name} with {extractor.__name__}: {exc}", file=sys.stderr)

    return parse_single_snippet(path, source)


def write_category_storage(category: dict, problems: list[ProblemRecord]) -> dict:
    storage_problems = [build_storage_problem(category, problem) for problem in problems]
    category_storage = {
        "category_id": category["id"],
        "category_name": category["name"],
        "sequence": category["sequence"],
        "source_reference": category["source_reference"],
        "problems": storage_problems,
    }

    category_filename = f"{category['sequence']:02d}_{category['id']}.json"
    category_path = PROBLEM_BANK_CATEGORIES_DIR / category_filename
    category_path.write_text(json.dumps(category_storage, indent=2))

    return {
        "id": category["id"],
        "name": category["name"],
        "sequence": category["sequence"],
        "file": f"categories/{category_filename}",
        "problem_count": len(storage_problems),
        "source_reference": category["source_reference"],
    }


def build_problem_bank() -> dict:
    PROBLEM_BANK_CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    categories_index = []

    for path in sorted(REFERENCE_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue

        category = category_meta(path)
        problems = parse_category_file(path)
        categories_index.append(write_category_storage(category, problems))

    algo_buckets: dict[str, list[tuple[int, ProblemRecord]]] = {
        group: [] for group in ALGO_CATEGORY_CONFIG
    }
    for path in sorted(REFERENCE_ALGOS_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        group, order, problem = parse_algo_problem_file(path)
        algo_buckets[group].append((order, problem))

    for group, config in sorted(ALGO_CATEGORY_CONFIG.items(), key=lambda item: item[1]["sequence"]):
        bucket = sorted(algo_buckets.get(group, []), key=lambda item: (item[0], item[1].title))
        if not bucket:
            continue

        problems = []
        for sequence, (_, problem) in enumerate(bucket, start=1):
            problem.sequence = sequence
            problems.append(problem)

        category = {
            "id": config["id"],
            "name": config["name"],
            "sequence": config["sequence"],
            "source_reference": f"algos/{group}",
        }
        categories_index.append(write_category_storage(category, problems))

    index = {"categories": categories_index}
    PROBLEM_BANK_DIR.mkdir(parents=True, exist_ok=True)
    (PROBLEM_BANK_DIR / "index.json").write_text(json.dumps(index, indent=2))
    return index


def main() -> None:
    index = build_problem_bank()
    total_categories = len(index["categories"])
    total_problems = sum(category["problem_count"] for category in index["categories"])
    print(f"Built problem bank with {total_categories} categories and {total_problems} problems.")


if __name__ == "__main__":
    main()
