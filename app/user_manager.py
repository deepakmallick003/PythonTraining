"""
User management for progress tracking and authentication
"""
import json
import os
from pathlib import Path
from datetime import datetime


class UserManager:
    """Manages user data, progress, and authentication"""
    
    APP_DIR = Path(__file__).resolve().parent
    DATA_DIR = APP_DIR / "data"
    USERS_FILE = DATA_DIR / "users.json"
    PROGRESS_FILE = DATA_DIR / "progress.json"
    
    def __init__(self):
        self.DATA_DIR.mkdir(exist_ok=True)
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create data files if they don't exist"""
        if not self.USERS_FILE.exists():
            with open(self.USERS_FILE, 'w') as f:
                json.dump([], f)
        
        if not self.PROGRESS_FILE.exists():
            with open(self.PROGRESS_FILE, 'w') as f:
                json.dump({}, f)
    
    def _read_users(self):
        """Read users from file"""
        with open(self.USERS_FILE, 'r') as f:
            return json.load(f)
    
    def _write_users(self, users):
        """Write users to file"""
        with open(self.USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _read_progress(self):
        """Read progress from file"""
        with open(self.PROGRESS_FILE, 'r') as f:
            return json.load(f)
    
    def _write_progress(self, progress):
        """Write progress to file"""
        with open(self.PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def user_exists(self, username):
        """Check if user exists"""
        users = self._read_users()
        return any(u['username'] == username for u in users)
    
    def create_user(self, username, password=None):
        """Create a new user"""
        if self.user_exists(username):
            return False
        
        users = self._read_users()
        users.append({
            'username': username,
            'password': password or username,  # Simple auth, no hashing
            'created_at': datetime.now().isoformat()
        })
        self._write_users(users)
        
        # Initialize progress for user
        progress = self._read_progress()
        progress[username] = {}
        self._write_progress(progress)
        
        return True
    
    def authenticate(self, username, password):
        """Authenticate user"""
        users = self._read_users()
        for user in users:
            if user['username'] == username:
                # Simple password check (no hashing for this demo)
                return user.get('password') == password or password == username
        return False
    
    def get_all_users(self):
        """Get all users"""
        return self._read_users()
    
    def delete_user(self, username):
        """Delete a user and their progress"""
        users = self._read_users()
        users = [u for u in users if u['username'] != username]
        self._write_users(users)
        
        progress = self._read_progress()
        if username in progress:
            del progress[username]
        self._write_progress(progress)
        
        return True
    
    def reset_user_progress(self, username):
        """Reset user's solved problems"""
        progress = self._read_progress()
        if username in progress:
            progress[username] = {}
            self._write_progress(progress)
        return True
    
    def mark_problem_solved(self, username, problem_id):
        """Mark a problem as solved"""
        progress = self._read_progress()
        if username not in progress:
            progress[username] = {}
        
        progress[username][problem_id] = {
            'solved': True,
            'solved_at': datetime.now().isoformat()
        }
        self._write_progress(progress)
    
    def get_user_progress(self, username):
        """Get user's progress"""
        progress = self._read_progress()
        return progress.get(username, {})
    
    def is_problem_solved(self, username, problem_id):
        """Check if problem is solved"""
        progress = self.get_user_progress(username)
        return progress.get(problem_id, {}).get('solved', False)
