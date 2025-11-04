from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Database path configuration
DB_PATH = os.environ.get('DATABASE_PATH', 'tasks.db')

def init_db():
    """Initialize database with enhanced schema"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Enhanced tasks table
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'General',
                priority INTEGER DEFAULT 1,
                completed BOOLEAN NOT NULL DEFAULT 0,
                due_date TEXT,
                tags TEXT,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences table
        c.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme TEXT DEFAULT 'light',
                primary_color TEXT DEFAULT '#667eea',
                view_mode TEXT DEFAULT 'list',
                animation_intensity TEXT DEFAULT 'normal',
                first_visit BOOLEAN DEFAULT 1
            )
        ''')
        
        # Initialize default preferences if not exists
        c.execute('SELECT COUNT(*) FROM preferences')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO preferences (theme) VALUES (?)', ('light',))
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def index():
    return render_template('nexatask.html')

# API Routes
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = []
        for row in c.fetchall():
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'category': row[3],
                'priority': row[4],
                'completed': bool(row[5]),
                'due_date': row[6],
                'tags': json.loads(row[7]) if row[7] else [],
                'completed_at': row[8],
                'created_at': row[9]
            })
        conn.close()
        return jsonify(tasks)
    except Exception as e:
        print(f"Error getting tasks: {e}")
        # Reinitialize database and try again
        init_db()
        return jsonify([])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        category = data.get('category', 'General')
        priority = data.get('priority', 1)
        due_date = data.get('due_date')
        tags = json.dumps(data.get('tags', []))
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO tasks 
                     (title, description, category, priority, due_date, tags) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (title, description, category, priority, due_date, tags))
        conn.commit()
        task_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'id': task_id,
            'title': title,
            'description': description,
            'category': category,
            'priority': priority,
            'completed': False,
            'due_date': due_date,
            'tags': json.loads(tags)
        })
    except Exception as e:
        print(f"Error adding task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if 'completed' in data:
            completed = data.get('completed')
            completed_at = datetime.now().isoformat() if completed else None
            c.execute('UPDATE tasks SET completed = ?, completed_at = ? WHERE id = ?',
                      (completed, completed_at, task_id))
        else:
            # Update other fields
            title = data.get('title')
            description = data.get('description')
            category = data.get('category')
            priority = data.get('priority')
            due_date = data.get('due_date')
            tags = json.dumps(data.get('tags', []))
            
            c.execute('''UPDATE tasks SET 
                         title = ?, description = ?, category = ?, 
                         priority = ?, due_date = ?, tags = ?
                         WHERE id = ?''',
                      (title, description, category, priority, due_date, tags, task_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({'error': str(e)}), 500

# Analytics API
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Total tasks
        c.execute('SELECT COUNT(*) FROM tasks')
        total_tasks = c.fetchone()[0]
        
        # Completed tasks
        c.execute('SELECT COUNT(*) FROM tasks WHERE completed = 1')
        completed_tasks = c.fetchone()[0]
        
        # Completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Tasks by category
        c.execute('SELECT category, COUNT(*) FROM tasks GROUP BY category')
        tasks_by_category = {row[0]: row[1] for row in c.fetchall()}
        
        # Tasks by priority
        c.execute('SELECT priority, COUNT(*) FROM tasks GROUP BY priority')
        tasks_by_priority = {row[0]: row[1] for row in c.fetchall()}
        
        # Recent activity (last 7 days)
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        c.execute('''SELECT DATE(completed_at) as date, COUNT(*) 
                     FROM tasks 
                     WHERE completed = 1 AND completed_at >= ?
                     GROUP BY DATE(completed_at)''', (week_ago,))
        daily_completions = {row[0]: row[1] for row in c.fetchall()}
        
        # Productivity streak
        c.execute('''SELECT completed_at FROM tasks 
                     WHERE completed = 1 
                     ORDER BY completed_at DESC''')
        completed_dates = [row[0] for row in c.fetchall() if row[0]]
        streak = calculate_streak(completed_dates)
        
        conn.close()
        
        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': total_tasks - completed_tasks,
            'completion_rate': round(completion_rate, 1),
            'tasks_by_category': tasks_by_category,
            'tasks_by_priority': tasks_by_priority,
            'daily_completions': daily_completions,
            'productivity_streak': streak
        })
    except Exception as e:
        print(f"Error getting analytics: {e}")
        return jsonify({
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'completion_rate': 0,
            'tasks_by_category': {},
            'tasks_by_priority': {},
            'daily_completions': {},
            'productivity_streak': 0
        })

# Preferences API
@app.route('/api/preferences', methods=['GET'])
def get_preferences():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM preferences LIMIT 1')
        row = c.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'theme': row[1],
                'primary_color': row[2],
                'view_mode': row[3],
                'animation_intensity': row[4],
                'first_visit': bool(row[5])
            })
        return jsonify({
            'theme': 'light',
            'primary_color': '#667eea',
            'view_mode': 'list',
            'animation_intensity': 'normal',
            'first_visit': True
        })
    except Exception as e:
        print(f"Error getting preferences: {e}")
        return jsonify({
            'theme': 'light',
            'primary_color': '#667eea',
            'view_mode': 'list',
            'animation_intensity': 'normal',
            'first_visit': True
        })

@app.route('/api/preferences', methods=['PUT'])
def update_preferences():
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''UPDATE preferences SET 
                     theme = ?, primary_color = ?, view_mode = ?, 
                     animation_intensity = ?, first_visit = ?
                     WHERE id = 1''',
                  (data.get('theme'), data.get('primary_color'),
                   data.get('view_mode'), data.get('animation_intensity'),
                   data.get('first_visit', 0)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating preferences: {e}")
        return jsonify({'error': str(e)}), 500

def calculate_streak(completed_dates):
    """Calculate current productivity streak"""
    if not completed_dates:
        return 0
    
    streak = 0
    current_date = datetime.now().date()
    
    for date_str in completed_dates:
        date = datetime.fromisoformat(date_str).date()
        if date == current_date or date == current_date - timedelta(days=streak):
            streak += 1
            current_date = date
        else:
            break
    
    return streak

# Initialize database on app startup (works with both Flask dev server and gunicorn)
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
