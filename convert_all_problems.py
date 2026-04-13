#!/usr/bin/env python3
"""
Script to convert reference/pythonbasics problems to JSON format
"""
import os
import re
import json
import ast

def parse_problem_block(block):
    """Parse a single problem block from the reference file"""
    lines = [line.strip() for line in block.split('\n') if line.strip()]

    problem = {}

    # Extract title from first print statement
    for line in lines:
        if line.startswith('# print("') and 'Question' in line:
            title_match = re.search(r'# print\("([^"]+)"\)', line)
            if title_match:
                problem['title'] = title_match.group(1)
                break

    # Extract expected output
    for line in lines:
        if 'Expected output:' in line:
            expected_match = re.search(r"Expected output: '([^']+)'", line)
            if expected_match:
                problem['expected_output'] = expected_match.group(1)
                break

    # Extract input setup (variable assignments)
    input_setup = []
    solution_code = []

    for line in lines:
        # Variable assignments (not comments, not print statements)
        if not line.startswith('#') and '=' in line and not 'print' in line:
            input_setup.append(line)

        # Extract code from print statements
        if 'print(text[' in line and not line.startswith('#'):
            # This line contains the actual code
            code_match = re.search(r'print\(([^)]+)\)', line)
            if code_match:
                solution_code.append(code_match.group(1))

    problem['input_setup'] = '\n'.join(input_setup)
    problem['solution_code'] = '\n'.join(solution_code) if solution_code else 'print(text[4])'

    return problem

def parse_reference_file(filepath):
    """Parse a reference file and extract all problems"""
    problems = []

    with open(filepath, 'r') as f:
        lines = f.readlines()

    current_problem = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Start of a new problem - handle both formats
        if (line.startswith('# print("') and 'Question' in line) or \
           (line.startswith('print("') and 'Question' in line and not line.startswith('#')):
            if current_problem:
                problems.append(current_problem)

            current_problem = {}

            # Extract title
            if line.startswith('# print("'):
                title_match = re.search(r'# print\("([^"]+)"\)', line)
            else:
                title_match = re.search(r'print\("([^"]+)"\)', line)
            if title_match:
                current_problem['title'] = title_match.group(1)

            # Look for expected output in next few lines
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j].strip()
                if 'Expected output:' in next_line:
                    expected_match = re.search(r"Expected output: ([^\]]+\]|[^']+'|[^\)]+\))", next_line)
                    if expected_match:
                        current_problem['expected_output'] = expected_match.group(1).strip()
                    break

        # Variable assignments (input setup) - handle both commented and uncommented
        elif ('= ' in line or ' = ' in line) and not 'print' in line and not 'Expected output:' in line:
            if current_problem:
                if 'input_setup' not in current_problem:
                    current_problem['input_setup'] = []
                # Remove comment marker if present
                clean_line = line.lstrip('#').strip()
                current_problem['input_setup'].append(clean_line)

        # Code lines - look for actual code execution
        elif ('append(' in line or 'clear(' in line or 'text[' in line or any(op in line for op in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>='])) and not line.startswith('print') and not 'Expected output:' in line:
            if current_problem and 'solution_code' not in current_problem:
                current_problem['solution_code'] = line

        i += 1

    # Add the last problem
    if current_problem:
        problems.append(current_problem)

    # Convert input_setup to string
    for problem in problems:
        if 'input_setup' in problem:
            problem['input_setup'] = '\n'.join(problem['input_setup'])
        else:
            problem['input_setup'] = ''

        if 'solution_code' not in problem:
            # Try to infer from the problem type
            if 'append' in problem.get('title', '').lower():
                problem['solution_code'] = 'nums.append(4)'
            elif 'clear' in problem.get('title', '').lower():
                problem['solution_code'] = 'nums.clear()'
            else:
                problem['solution_code'] = 'print("solution")'  # fallback

    return problems

def get_category_name(filename):
    """Get category name from filename"""
    category_map = {
        '01_strings.py': 'Strings',
        '02_list.py': 'Lists',
        '03_tuple.py': 'Tuples',
        '04_set.py': 'Sets',
        '05_dictionary.py': 'Dictionaries',
        '06_variables.py': 'Variables',
        '07_datatypes.py': 'DataTypes',
        '08_operators.py': 'Operators',
        '09_operators-precedence.py': 'OperatorPrecedence',
        '10_numbersystem-conversion.py': 'NumberSystemConversion',
        '11_bitwise.py': 'Bitwise',
        '12_user-input.py': 'UserInput',
        '13_loop-breakers.py': 'LoopBreakers',
        '14_arrays.py': 'Arrays',
        '15_numpy-1.py': 'NumPy1',
        '16_numpy-2.py': 'NumPy2',
        '17_numpy_matrix.py': 'NumPyMatrix',
        '18_functions-argument-types.py': 'FunctionsArgumentTypes',
        '19_function-global-keyword.py': 'FunctionGlobalKeyword',
        '20_functions-mutable-immutable.py': 'FunctionsMutableImmutable',
        '21_lambda.py': 'Lambda',
        '22_decorator.py': 'Decorator',
        '23_underscore-and-dunder.py': 'UnderscoreDunder',
        '24_special_variable_name.py': 'SpecialVariableName',
        '25_methodtypes.py': 'MethodTypes',
        '26_innerclass.py': 'InnerClass',
        '27_inheritance_types.py': 'InheritanceTypes',
        '28_inheritance_order.py': 'InheritanceOrder',
        '29_polymorphism-ducktyping.py': 'PolymorphismDuckTyping'
    }

    return category_map.get(filename, filename.replace('.py', '').replace('_', ' ').title())

def create_json_problem(problem, category, index):
    """Create JSON structure for a problem"""
    problem_id = f"{category.lower()}_{index:02d}_{re.sub(r'[^a-zA-Z0-9_]', '_', problem['title'].lower().replace(' ', '_').replace('-', '_'))}"

    # Create full solution code with proper structure
    input_setup = problem.get('input_setup', '')
    solution_code = problem.get('solution_code', 'print(text[4])')

    # Create full solution with main function and imports if needed
    full_solution = f"""# Solution
{input_setup}
{solution_code}
"""

    # Create starter code (what user sees initially)
    starter_code = f"""# Write your code here
{solution_code}
"""

    # Create description with example input/output
    example_input = problem.get('input_setup', 'text = "HelloWorld"')
    example_output = problem.get('expected_output', 'o')

    description = f"""Example Input:
{example_input}

Example Output:
{example_output}
"""

    json_problem = {
        "id": problem_id,
        "title": problem['title'],
        "category": category,
        "difficulty": "Easy",
        "description": description,
        "example_input": example_input,
        "example_output": example_output,
        "starter_code": starter_code,
        "solution": full_solution,
        "test_cases": [
            {
                "input": input_setup,
                "expected_output": problem.get('expected_output', '')
            }
        ]
    }

    return json_problem

def main():
    """Main conversion function"""
    reference_dir = '/Users/deepak/PythonTraining/reference/pythonbasics'
    output_dir = '/Users/deepak/PythonTraining/app/problems'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each reference file
    for filename in sorted(os.listdir(reference_dir)):
        if not filename.endswith('.py') or filename == '__init__.py':
            continue

        filepath = os.path.join(reference_dir, filename)
        category = get_category_name(filename)

        print(f"Processing {filename} -> {category}")

        problems = parse_reference_file(filepath)

        for i, problem in enumerate(problems, 1):
            json_problem = create_json_problem(problem, category, i)

            # Write JSON file
            output_file = os.path.join(output_dir, f"{json_problem['id']}.json")
            with open(output_file, 'w') as f:
                json.dump(json_problem, f, indent=2)

            print(f"  Created {json_problem['id']}.json")

if __name__ == '__main__':
    main()