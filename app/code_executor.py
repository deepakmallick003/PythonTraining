"""
Safe code execution module with timeout and error handling
"""
import sys
import io
import subprocess
import tempfile
import os
from contextlib import redirect_stdout, redirect_stderr

class CodeExecutor:
    """Executes user code safely with timeout and output capture"""
    TEST_MODULE_NAME = "__coding_practice_test__"
    
    @staticmethod
    def execute(code, timeout=5, test_cases=None):
        """
        Execute code safely and return output or error
        
        Args:
            code (str): Python code to execute
            timeout (int): Timeout in seconds
            test_cases (list): List of test cases with 'input' and 'expected_output'
            
        Returns:
            dict: For test cases: {'status': 'success'|'error', 'results': [...], 'passed': int, 'total': int}
                  For simple execution: {'status': 'success'|'error', 'output': str, 'error': str}
        """
        # If test cases provided, run validation mode
        if test_cases:
            return CodeExecutor._run_test_cases(code, test_cases, timeout)
        
        # Otherwise run simple execution mode
        try:
            # Create a temporary file to execute the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run the code in a subprocess with timeout
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    return {
                        'status': 'success',
                        'output': output if output else '(No output)',
                        'error': None
                    }
                else:
                    error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                    return {
                        'status': 'error',
                        'output': None,
                        'error': error_msg
                    }
            finally:
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'output': None,
                'error': f'Code execution timed out (>{timeout}s). Check for infinite loops.'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': None,
                'error': f'Execution error: {str(e)}'
            }
    
    @staticmethod
    def _run_test_cases(code, test_cases, timeout=5):
        """
        Run code against multiple test cases and validate output
        
        Args:
            code (str): Python code to execute (should define variables/functions from test input)
            test_cases (list): List of dicts with 'input' and 'expected_output'
            timeout (int): Timeout per test case
            
        Returns:
            dict: {'status': 'success'|'error', 'results': [...], 'passed': int, 'total': int, 'error': str or None}
        """
        results = []
        passed_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            test_input = test_case.get('input', '')
            test_call = test_case.get('call', '')
            expected_output = test_case.get('expected_output', '').strip()
            
            # Disable sample __main__ runners in generated starter/solution code,
            # then append the per-test setup and invocation explicitly.
            parts = [
                f'__name__ = "{CodeExecutor.TEST_MODULE_NAME}"',
                code,
            ]
            if test_input.strip():
                parts.append(test_input)
            if test_call.strip():
                parts.append(test_call)
            full_code = '\n\n'.join(part for part in parts if part.strip())
            
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(full_code)
                    temp_file = f.name
                
                try:
                    # Run the code
                    result = subprocess.run(
                        [sys.executable, temp_file],
                        capture_output=True,
                        text=True,
                        timeout=timeout
                    )
                    
                    actual_output = result.stdout.strip()
                    
                    if result.returncode == 0:
                        # Compare outputs
                        passed = actual_output == expected_output
                        if passed:
                            passed_count += 1
                        
                        results.append({
                            'test_num': i,
                            'status': 'PASS' if passed else 'FAIL',
                            'input': test_input[:100] + ('...' if len(test_input) > 100 else ''),
                            'expected': expected_output[:100] + ('...' if len(expected_output) > 100 else ''),
                            'actual': actual_output[:100] + ('...' if len(actual_output) > 100 else '') if actual_output else '(No output)',
                            'error': None
                        })
                    else:
                        # Execution error
                        error_msg = result.stderr.strip() if result.stderr else 'Unknown error'
                        results.append({
                            'test_num': i,
                            'status': 'ERROR',
                            'input': test_input[:100] + ('...' if len(test_input) > 100 else ''),
                            'expected': expected_output[:100] + ('...' if len(expected_output) > 100 else ''),
                            'actual': None,
                            'error': error_msg[:200] + ('...' if len(error_msg) > 200 else '')
                        })
                
                finally:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                        
            except subprocess.TimeoutExpired:
                results.append({
                    'test_num': i,
                    'status': 'TIMEOUT',
                    'input': test_input[:100] + ('...' if len(test_input) > 100 else ''),
                    'expected': expected_output[:100] + ('...' if len(expected_output) > 100 else ''),
                    'actual': None,
                    'error': f'Execution timed out (>{timeout}s)'
                })
            except Exception as e:
                results.append({
                    'test_num': i,
                    'status': 'ERROR',
                    'input': test_input[:100] + ('...' if len(test_input) > 100 else ''),
                    'expected': expected_output[:100] + ('...' if len(expected_output) > 100 else ''),
                    'actual': None,
                    'error': str(e)[:200]
                })
        
        overall_status = 'success' if passed_count == len(test_cases) else 'error'
        
        return {
            'status': overall_status,
            'results': results,
            'passed': passed_count,
            'total': len(test_cases),
            'error': None if overall_status == 'success' else f'Failed {len(test_cases) - passed_count} out of {len(test_cases)} test cases'
        }
    
    @staticmethod
    def validate_syntax(code):
        """
        Validate Python code syntax without executing
        
        Args:
            code (str): Python code to validate
            
        Returns:
            dict: {'valid': bool, 'error': str or None}
        """
        try:
            compile(code, '<string>', 'exec')
            return {'valid': True, 'error': None}
        except SyntaxError as e:
            return {
                'valid': False,
                'error': f'Syntax Error at line {e.lineno}: {e.msg}\n{e.text}'
            }
        except Exception as e:
            return {'valid': False, 'error': f'Error: {str(e)}'}
