from flask import Blueprint, render_template, request, url_for, flash, redirect
from app import db
from app.models import Task
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.view_tasks'))
    return redirect(url_for('auth.login'))


@tasks_bp.route('/tasks')
@login_required
def view_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_tasks():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='Pending', user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    else:
        flash('Task title required', 'warning')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_status(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
        flash('Task status updated', 'success')
    else:
        flash('Task not found or not authorized', 'danger')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found or unauthorized.', 'danger')

    return redirect(url_for('tasks.view_tasks'))