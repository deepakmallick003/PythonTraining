"""
Flask routes for the application
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .problem_loader import ProblemLoader
from .code_executor import CodeExecutor
from .user_manager import UserManager

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize user manager
user_manager = UserManager()

def _get_current_user():
    """Get current logged in user from session"""
    return session.get('user')

def _get_navigation_data(problem_id):
    """Get navigation data for prev/next problem and category"""
    problem = ProblemLoader.get_problem(problem_id)
    if not problem:
        return {}
    
    category_id = problem.get('category_id')
    category = ProblemLoader.get_category(category_id)
    if not category:
        return {}
    
    problems = category.get('problems', [])
    problem_indices = {p['id']: i for i, p in enumerate(problems)}
    current_idx = problem_indices.get(problem_id, 0)
    
    nav = {
        'category_id': category_id,
        'prev_problem_id': problems[current_idx - 1]['id'] if current_idx > 0 else None,
        'next_problem_id': problems[current_idx + 1]['id'] if current_idx < len(problems) - 1 else None,
    }
    
    # Get prev/next category
    categories = ProblemLoader.get_categories()
    category_indices = {c['id']: i for i, c in enumerate(categories)}
    current_cat_idx = category_indices.get(category_id, 0)
    
    nav['prev_category_id'] = categories[current_cat_idx - 1]['id'] if current_cat_idx > 0 else None
    nav['next_category_id'] = categories[current_cat_idx + 1]['id'] if current_cat_idx < len(categories) - 1 else None
    
    return nav

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username:
            return render_template('login.html', error='Username required')
        
        # Auto-create user if doesn't exist (for demo purposes)
        if not user_manager.user_exists(username):
            user_manager.create_user(username, password)
        
        # Authenticate
        if user_manager.authenticate(username, password):
            session['user'] = username
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html', error=None)

@main_bp.route('/logout')
def logout():
    """Logout user"""
    session.pop('user', None)
    return redirect(url_for('main.login'))

@main_bp.route('/settings')
def settings():
    """Settings and admin page"""
    user = _get_current_user()
    if not user:
        return redirect(url_for('main.login'))
    
    all_users = user_manager.get_all_users()
    user_progress = {}
    for u in all_users:
        progress = user_manager.get_user_progress(u['username'])
        user_progress[u['username']] = len([p for p in progress.values() if p.get('solved')])
    
    return render_template('settings.html', users=all_users, user_progress=user_progress, current_user=user)

@main_bp.route('/')
def index():
    """Main page - category list"""
    user = _get_current_user()
    if not user:
        return redirect(url_for('main.login'))
    
    categories = ProblemLoader.get_categories()
    return render_template('index.html', categories=categories, current_user=user)

@main_bp.route('/category/<category_id>')
def category(category_id):
    """Category page - problems in category"""
    user = _get_current_user()
    if not user:
        return redirect(url_for('main.login'))
    
    category_data = ProblemLoader.get_category(category_id)
    if not category_data:
        return render_template('404.html'), 404
    problems = ProblemLoader.get_problems_by_category(category_id)
    
    # Add solved status
    for p in problems:
        p['solved'] = user_manager.is_problem_solved(user, p['id'])
    
    # Get navigation data
    categories = ProblemLoader.get_categories()
    current_index = next((i for i, c in enumerate(categories) if c['id'] == category_id), -1)
    prev_category = categories[current_index - 1] if current_index > 0 else None
    next_category = categories[current_index + 1] if current_index < len(categories) - 1 else None
    
    return render_template('category.html', category=category_data, problems=problems, current_user=user, prev_category=prev_category, next_category=next_category)

@main_bp.route('/problem/<problem_id>')
def problem(problem_id):
    """Problem detail page"""
    user = _get_current_user()
    if not user:
        return redirect(url_for('main.login'))
    
    problem_data = ProblemLoader.get_problem(problem_id)
    if not problem_data:
        return render_template('404.html'), 404

    problem_data['solved'] = user_manager.is_problem_solved(user, problem_id)
    problem_data['saved_code'] = user_manager.get_saved_code(user, problem_id)
    problem_data['nav'] = _get_navigation_data(problem_id)

    return render_template('problem.html', problem=problem_data, current_user=user)


# API Routes
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all problem categories"""
    categories = ProblemLoader.get_categories()
    return jsonify(categories)

@api_bp.route('/category/<category_id>', methods=['GET'])
def get_category_problems(category_id):
    """Get problems in a category"""
    problems = ProblemLoader.get_problems_by_category(category_id)
    return jsonify(problems)

@api_bp.route('/problems', methods=['GET'])
def get_problems():
    """Get all problems"""
    problems = ProblemLoader.get_all_problems()
    return jsonify(problems)

@api_bp.route('/problem/<problem_id>', methods=['GET'])
def get_problem(problem_id):
    """Get problem details"""
    problem = ProblemLoader.get_problem(problem_id)
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    return jsonify(problem)

@api_bp.route('/run', methods=['POST'])
def run_code():
    """Execute user code with optional test case validation"""
    data = request.get_json()
    code = data.get('code', '')
    test_cases = data.get('test_cases', None)
    problem_id = data.get('problem_id', None)
    
    if not code.strip():
        return jsonify({
            'status': 'error',
            'output': None,
            'error': 'Code cannot be empty'
        })
    
    # Execute the code with test cases if provided
    result = CodeExecutor.execute(code, test_cases=test_cases)
    
    # Save the successful code state for this problem if it ran cleanly
    user = _get_current_user()
    if user and problem_id and result.get('status') == 'success':
        user_manager.save_problem_code(user, problem_id, code)

    # Mark problem as solved if all tests pass
    if user and result.get('status') == 'success' and test_cases and problem_id:
        if result.get('passed') == result.get('total'):
            user_manager.mark_problem_solved(user, problem_id)
            result['problem_marked_solved'] = True
    
    return jsonify(result)

@api_bp.route('/validate', methods=['POST'])
def validate_code():
    """Validate code syntax"""
    data = request.get_json()
    code = data.get('code', '')
    
    result = CodeExecutor.validate_syntax(code)
    return jsonify(result)

@api_bp.route('/progress/<problem_id>', methods=['POST'])
def save_progress(problem_id):
    """Save user progress for a problem"""
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if data.get('solved'):
        user_manager.mark_problem_solved(user, problem_id)
        return jsonify({'status': 'success', 'solved': True})
    
    return jsonify({'status': 'success'})

@api_bp.route('/user/settings/delete-user', methods=['POST'])
def delete_user_endpoint():
    """Delete a user (admin only)"""
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    target_user = data.get('username')
    
    if target_user:
        user_manager.delete_user(target_user)
        return jsonify({'status': 'success'})
    
    return jsonify({'error': 'No user specified'}), 400

@api_bp.route('/user/settings/reset-progress', methods=['POST'])
def reset_user_progress():
    """Reset user's progress"""
    user = _get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    target_user = data.get('username', user)
    
    user_manager.reset_user_progress(target_user)
    return jsonify({'status': 'success'})
