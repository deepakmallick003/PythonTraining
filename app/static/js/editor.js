/* Editor JavaScript with Test Case Support */
document.addEventListener('DOMContentLoaded', function() {
    const codeEditor = document.getElementById('codeEditor');
    const runBtn = document.getElementById('runBtn');
    const resetBtn = document.getElementById('resetBtn');
    const solutionBtn = document.getElementById('solutionBtn');
    const output = document.getElementById('output');
    const testResults = document.getElementById('testResults');
    const outputText = document.getElementById('outputText');
    const closeOutput = document.getElementById('closeOutput');
    const closeResults = document.getElementById('closeResults');
    const charCount = document.getElementById('charCount');

    let editorInstance = null;

    if (window.CodeMirror) {
        editorInstance = CodeMirror.fromTextArea(codeEditor, {
            mode: { name: 'python', version: 3 },
            theme: 'material-darker',
            lineNumbers: true,
            lineWrapping: false,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            autoCloseBrackets: true,
            matchBrackets: true,
            viewportMargin: Infinity
        });
        editorInstance.setSize('100%', '100%');
    }

    function getEditorValue() {
        return editorInstance ? editorInstance.getValue() : codeEditor.value;
    }

    function setEditorValue(value) {
        if (editorInstance) {
            editorInstance.setValue(value);
            editorInstance.focus();
        } else {
            codeEditor.value = value;
        }
    }

    // Get problem ID from URL
    const problemId = window.location.pathname.split('/').pop();
    const starterCode = getEditorValue();
    
    // Fetch problem data to get test cases
    let problemData = {};
    let defaultRunLabel = '<i class="fas fa-play"></i> Run Tests';

    function updateRunButtonLabel() {
        const hasTests = (problemData.test_cases || []).length > 0;
        defaultRunLabel = hasTests
            ? '<i class="fas fa-play"></i> Run Tests'
            : '<i class="fas fa-play"></i> Run Code';
        runBtn.innerHTML = defaultRunLabel;
    }

    fetch(`/api/problem/${problemId}`)
        .then(r => r.json())
        .then(data => {
            problemData = data;
            updateRunButtonLabel();
        });
    
    // Update character count
    function updateCharCount() {
        const count = getEditorValue().length;
        charCount.textContent = `${count} characters`;
    }

    if (editorInstance) {
        editorInstance.on('change', updateCharCount);
    } else {
        codeEditor.addEventListener('input', updateCharCount);
    }
    updateCharCount();

    if (window.hljs) {
        hljs.highlightAll();
    }

    // Run code/tests
    runBtn.addEventListener('click', async function() {
        const code = getEditorValue();
        
        if (!code.trim()) {
            showOutput('Error: Code cannot be empty', 'error');
            return;
        }
        
        runBtn.disabled = true;
        runBtn.textContent = 'Running...';
        
        try {
            // Check if problem has test cases
            const testCases = problemData.test_cases || [];
            
            const response = await fetch('/api/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    code,
                    test_cases: testCases.length > 0 ? testCases : null,
                    problem_id: problemId
                })
            });
            
            const data = await response.json();
            
            if (testCases.length > 0 && data.results) {
                // Show test results
                showTestResults(data);
                
                // Mark as solved if all tests pass
                if (data.status === 'success' && data.passed === data.total) {
                    markProblemSolved();
                }
            } else if (data.status === 'success') {
                showOutput(data.output || '(No output)', 'success');
            } else {
                showOutput(data.error || 'Unknown error', 'error');
            }
        } catch (error) {
            showOutput(`Error: ${error.message}`, 'error');
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = defaultRunLabel;
        }
    });
    
    // Mark problem as solved
    function markProblemSolved() {
        fetch(`/api/progress/${problemId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ solved: true })
        }).then(() => {
            // Show success indicator
            const badge = document.querySelector('.solved-badge');
            if (!badge) {
                // Add solved badge to page if not present
                const header = document.querySelector('h1');
                if (header) {
                    const span = document.createElement('span');
                    span.className = 'solved-badge';
                    span.innerHTML = '<i class="fas fa-check-circle"></i>';
                    header.appendChild(span);
                }
            }
        });
    }
    
    // Show test results
    function showTestResults(data) {
        output.style.display = 'none';
        testResults.style.display = 'block';
        
        const summary = document.getElementById('testResultsSummary');
        const container = document.getElementById('testCasesContainer');
        
        const { passed, total, results } = data;
        const allPassed = passed === total;
        
        // Summary
        summary.innerHTML = `
            <div class="test-summary">
                <span class="test-count">
                    <i class="fas fa-${allPassed ? 'check' : 'exclamation'}"></i>
                    ${passed}/${total} test cases passed
                </span>
                <span class="test-percentage ${allPassed ? 'pass' : 'fail'}">
                    ${Math.round((passed / total) * 100)}%
                </span>
            </div>
        `;
        
        // Individual test cases
        container.innerHTML = results.map((result, idx) => {
            const statusClasses = {
                'PASS': 'test-pass',
                'FAIL': 'test-fail',
                'ERROR': 'test-error',
                'TIMEOUT': 'test-timeout'
            };
            
            return `
                <div class="test-case ${statusClasses[result.status]}">
                    <div class="test-header">
                        <span class="test-status">
                            <i class="fas fa-${result.status === 'PASS' ? 'check' : 'times'}"></i>
                            Test #${result.test_num}: ${result.status}
                        </span>
                    </div>
                    <div class="test-details">
                        <div class="test-input">
                            <strong>Input:</strong>
                            <pre><code>${escapeHtml(result.input)}</code></pre>
                        </div>
                        <div class="test-output-row">
                            <div class="test-expected">
                                <strong>Expected:</strong>
                                <pre><code>${escapeHtml(result.expected)}</code></pre>
                            </div>
                            <div class="test-actual">
                                <strong>Actual:</strong>
                                <pre><code>${escapeHtml(result.actual || result.error || '(No output)')}</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        testResults.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Show simple output
    function showOutput(text, type) {
        testResults.style.display = 'none';
        outputText.textContent = text;
        output.className = `output ${type}`;
        output.style.display = 'block';
        output.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Close output
    closeOutput.addEventListener('click', function() {
        output.style.display = 'none';
    });
    
    if (closeResults) {
        closeResults.addEventListener('click', function() {
            testResults.style.display = 'none';
        });
    }
    
    // Reset code
    resetBtn.addEventListener('click', function() {
        document.getElementById('confirmModal').style.display = 'flex';
    });
    
    document.getElementById('confirmResetBtn').addEventListener('click', function() {
        setEditorValue(starterCode);
        updateCharCount();
        output.style.display = 'none';
        testResults.style.display = 'none';
        document.getElementById('confirmModal').style.display = 'none';
    });
    
    // Show solution
    solutionBtn.addEventListener('click', function() {
        const modal = document.getElementById('solutionModal');
        modal.style.display = 'flex';
        
        // Highlight code
        const codeBlock = modal.querySelector('code');
        hljs.highlightElement(codeBlock);
    });
    
    // Theme toggle for solution modal
    let isDarkTheme = true;
    const themeToggle = document.getElementById('themeToggle');
    const solutionCodeElement = document.getElementById('solutionCode');
    
    themeToggle.addEventListener('click', function() {
        isDarkTheme = !isDarkTheme;
        const codeBlock = solutionCodeElement;
        
        if (isDarkTheme) {
            codeBlock.className = 'language-python';
            themeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark';
            themeToggle.className = 'btn btn-secondary';
        } else {
            codeBlock.className = 'language-python hljs';
            themeToggle.innerHTML = '<i class="fas fa-sun"></i> Light';
            themeToggle.className = 'btn btn-light';
        }
        
        // Re-highlight
        hljs.highlightElement(codeBlock);
    });
    
    // Close solution modal
    document.getElementById('closeSolutionModal').addEventListener('click', function() {
        document.getElementById('solutionModal').style.display = 'none';
    });
    
    // Copy solution
    document.getElementById('copySolutionBtn').addEventListener('click', function() {
        const solutionCode = document.getElementById('solutionCode').textContent;
        navigator.clipboard.writeText(solutionCode).then(() => {
            const btn = this;
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                btn.innerHTML = originalText;
            }, 2000);
        });
    });
    
    // Apply solution
    document.getElementById('applySolutionBtn').addEventListener('click', function() {
        const solutionCode = document.getElementById('solutionCode').textContent;
        setEditorValue(solutionCode);
        updateCharCount();
        document.getElementById('solutionModal').style.display = 'none';
        showOutput('Solution applied to editor!', 'success');
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        ['solutionModal', 'confirmModal'].forEach(id => {
            const modal = document.getElementById(id);
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Helper function to escape HTML
    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
