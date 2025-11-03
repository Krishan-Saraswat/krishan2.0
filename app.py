from flask import Flask, render_template, request, jsonify
from models.db_models import db, Thought, Task
from routes import register_all_routes
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

register_all_routes(app)

@app.route('/', methods=['GET'])
def index():
    thought = Thought.query.order_by(Thought.id.desc()).first()
    tasks = Task.query.filter_by(created_date=date.today()).all()
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    return render_template('index.html', thought=thought.text if thought else "Thought of the Day", tasks=tasks, start_date=str(start_date), end_date=str(end_date))

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    new_thought = Thought(text=data['text'])
    db.session.add(new_thought)
    db.session.commit()
    return jsonify({'success': True, 'thought': new_thought.text})

@app.route('/remove', methods=['POST'])
def remove():
    thought = Thought.query.order_by(Thought.id.desc()).first()
    if thought:
        db.session.delete(thought)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(text=data['text'], created_date=date.today())
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'success': True, 'id': new_task.id, 'text': new_task.text, 'completed': new_task.completed})

@app.route('/toggle-task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        task.completed_date = date.today() if task.completed else None
        db.session.commit()
        return jsonify({'success': True, 'completed': task.completed})
    return jsonify({'success': False})

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(created_date=date.today()).all()
    pending = [{'id': t.id, 'text': t.text, 'completed': t.completed} for t in tasks if not t.completed]
    completed = [{'id': t.id, 'text': t.text, 'completed': t.completed} for t in tasks if t.completed]
    return jsonify({'pending': pending, 'completed': completed})

if __name__ == '__main__':
    app.run(debug=True)
