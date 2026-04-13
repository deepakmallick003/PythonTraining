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


BASE_DIR = Path(__file__).resolve().parent
REFERENCE_DIR = BASE_DIR / "reference" / "pythonbasics"
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
        "description": problem.prompt,
        "prompt": problem.prompt,
        "difficulty": problem.difficulty,
        "starter_code": problem.starter_code,
        "solution": problem.solution,
        "examples": problem.examples,
        "test_cases": problem.test_cases,
        "notes": problem.notes,
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


def derived_output_statements(block: list[ast.AST]) -> tuple[list[str], list[ast.AST]]:
    statements = []
    output_nodes: list[ast.AST] = []
    for node in block:
        text = first_print_text(node)
        if not text:
            continue
        stripped = text.strip()
        if not stripped.startswith(("Output", "Answer")):
            continue
        call = node.value
        extra_args = call.args[1:]
        if not extra_args:
            continue
        statements.append(f"print({', '.join(ast.unparse(arg) for arg in extra_args)})")
        output_nodes.extend(extra_args)
    return statements, output_nodes


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
        output_lines, output_expr_nodes = derived_output_statements(block)
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
        examples = []
        if not should_disable_tests(action_source):
            try:
                examples = [{"input": "Standalone snippet", "output": run_code_capture_output(action_source)}]
            except Exception:
                examples = []

        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=build_wrapped_code(import_lines, main_body=action_body),
                examples=examples,
                notes=["This problem is stored as a runnable standalone snippet."],
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
        notes = ["This category uses standalone demo snippets in the problem bank."]
        if "input(" in action_source or "sys.argv" in action_source:
            notes.append("Tests are disabled because this example expects live user input or command-line arguments.")

        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=build_wrapped_code(import_lines, main_body=action_body),
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
        prompt = title + "."
        action_source = "\n".join(block_lines).strip() + "\n"
        import_lines, action_body = split_imports_and_body(action_source)
        starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=prompt,
                sequence=sequence,
                starter_code=starter_code,
                solution=build_wrapped_code(import_lines, main_body=action_body),
                notes=["This section is stored as a standalone reference snippet."],
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
                problems.append(
                    ProblemRecord(
                        title=pretty_name(prompt.split(".")[0]),
                        prompt=prompt,
                        sequence=sequence,
                        starter_code=starter_code,
                        solution=build_wrapped_code(import_lines, main_body=action_body),
                        notes=["Stored as a runnable standalone snippet from the bitwise reference material."],
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
        problems.append(
            ProblemRecord(
                title=title_map.get(name, pretty_name(name)),
                prompt=title_map.get(name, pretty_name(name)) + ".",
                sequence=sequence,
                starter_code=build_wrapped_code([], parameter_names=[], placeholder=True),
                solution=build_wrapped_code([], main_body=action_source.strip()),
                notes=["Stored as a standalone wrapper demo from the underscore/dunder reference file."],
                source_reference={"file": path.name, "question": sequence},
            )
        )
        sequence += 1

    problems.append(
        ProblemRecord(
            title="Module __name__ Value",
            prompt="Print the module __name__ value.",
            sequence=sequence,
            starter_code=build_wrapped_code([], parameter_names=[], placeholder=True),
            solution=build_wrapped_code([], main_body="print(__name__)"),
            notes=["This mirrors the final __name__ line from the reference file."],
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
        problems.append(
            ProblemRecord(
                title=title,
                prompt=title + ".",
                sequence=sequence,
                starter_code=build_wrapped_code(import_lines, parameter_names=[], placeholder=True),
                solution=build_wrapped_code(import_lines, main_body=action_body),
                notes=["Stored as a standalone inheritance demo."],
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
        action_source = snippet[code_start:].strip() + "\n"
        import_lines, action_body = split_imports_and_body(action_source)
        problems.append(
            ProblemRecord(
                title=title,
                prompt=title + ".",
                sequence=sequence,
                starter_code=build_wrapped_code(import_lines, parameter_names=[], placeholder=True),
                solution=build_wrapped_code(import_lines, main_body=action_body),
                notes=["Stored as a standalone duck-typing snippet."],
                source_reference={"file": path.name, "question": sequence},
            )
        )
    return problems


def parse_single_snippet(path: Path, source: str) -> list[ProblemRecord]:
    title = TITLE_FROM_FILENAME_MAP.get(path.name, CATEGORY_NAME_MAP.get(path.name, pretty_name(path.stem)))
    prompt = title + "."
    import_lines, action_body = split_imports_and_body(source)
    starter_code = build_wrapped_code(import_lines, parameter_names=[], placeholder=True)
    return [
        ProblemRecord(
            title=title,
            prompt=prompt,
            sequence=1,
            starter_code=starter_code,
            solution=build_wrapped_code(import_lines, main_body=action_body),
            notes=["Stored as a standalone reference snippet."],
            source_reference={"file": path.name, "question": 1},
        )
    ]


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


def build_problem_bank() -> dict:
    PROBLEM_BANK_CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    categories_index = []

    for path in sorted(REFERENCE_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue

        category = category_meta(path)
        problems = parse_category_file(path)
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

        categories_index.append(
            {
                "id": category["id"],
                "name": category["name"],
                "sequence": category["sequence"],
                "file": f"categories/{category_filename}",
                "problem_count": len(storage_problems),
                "source_reference": category["source_reference"],
            }
        )

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
