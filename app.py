import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'quiz.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                q_type TEXT NOT NULL,
                content TEXT NOT NULL,
                options TEXT,
                answer TEXT
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                answers TEXT NOT NULL
            )
        ''')
        db.commit()

init_db()

@app.route('/')
def index():
    return render_template('quiz.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    db = get_db()
    if request.method == 'POST':
        # Calculate score
        questions = db.execute('SELECT * FROM questions').fetchall()
        score = 0
        total_mcq = 0
        user_answers = {}
        
        for q in questions:
            q_id = str(q['id'])
            user_answer = request.form.get(f'q_{q_id}')
            user_answers[q_id] = user_answer
            
            if q['q_type'] == 'mcq':
                total_mcq += 1
                if user_answer and user_answer.strip() == q['answer'].strip():
                    score += 1

        # Save result
        cur = db.execute('INSERT INTO results (score, total, answers) VALUES (?, ?, ?)',
                         (score, total_mcq, json.dumps(user_answers)))
        db.commit()
        return redirect(url_for('result', result_id=cur.lastrowid))

    questions = db.execute('SELECT * FROM questions').fetchall()
    # Parse options for MCQs
    processed_qs = []
    for q in questions:
        q_dict = dict(q)
        if q_dict['q_type'] == 'mcq' and q_dict['options']:
            try:
                q_dict['parsed_options'] = json.loads(q_dict['options'])
            except:
                q_dict['parsed_options'] = q_dict['options'].split(',')
        processed_qs.append(q_dict)

    return render_template('quiz.html', questions=processed_qs)

@app.route('/result/<int:result_id>')
def result(result_id):
    db = get_db()
    res = db.execute('SELECT * FROM results WHERE id = ?', (result_id,)).fetchone()
    if not res:
        return "Result not found", 404
    return render_template('result.html', result=res)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    if request.method == 'POST':
        q_type = request.form.get('q_type')
        content = request.form.get('content')
        if q_type == 'mcq':
            options = request.form.get('options')
            answer = request.form.get('answer')
            # Assuming options are comma separated, convert to JSON array
            opts_list = [o.strip() for o in options.split(',') if o.strip()]
            db.execute('INSERT INTO questions (q_type, content, options, answer) VALUES (?, ?, ?, ?)',
                       (q_type, content, json.dumps(opts_list), answer.strip()))
        elif q_type == 'code':
            db.execute('INSERT INTO questions (q_type, content) VALUES (?, ?)',
                       (q_type, content))
        db.commit()
        return redirect(url_for('admin'))
        
    questions = db.execute('SELECT * FROM questions').fetchall()
    results = db.execute('SELECT * FROM results ORDER BY id DESC').fetchall()
    return render_template('admin.html', questions=questions, results=results)

if __name__ == '__main__':
    app.run(debug=True)
