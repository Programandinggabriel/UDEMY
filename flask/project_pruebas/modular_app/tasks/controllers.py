from flask import Blueprint, render_template, request, redirect, url_for
from modular_app.tasks import sql_operations
from modular_app.tasks import forms

taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

@taskRoute.route('/')
def index():
    aTasks = sql_operations.getAllTask()
    return render_template('dashboard/task/index.html', tasks = aTasks)

@taskRoute.route('/create', methods=['POST', 'GET'])
def create():
    frm = forms.TaskForm()

    if frm.validate_on_submit():
        sql_operations.createTask(frm.name.data)
        
        return redirect(url_for('tasks.index'))
        #print(request.args.get('task'))

    return render_template('dashboard/task/create.html', form=frm)

@taskRoute.route('/<int:id>', methods=['GET'])
def show(id:int):
    task = sql_operations.getTaskById(taskId=id)

    return 'Mostrando task ' + task.name

@taskRoute.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id:int):
    oTask = sql_operations.getTaskById(id)
    frm = forms.TaskForm()
    
    if request.method == 'GET':
        frm.name.data = oTask.name
    elif request.method == 'POST':
        if frm.validate_on_submit():
            sql_operations.updateTask(taskId=id, taskName=frm.name.data)
            return redirect(url_for('tasks.index'))
    
    return render_template('dashboard/task/update.html', form=frm)

@taskRoute.route('/delete/<int:id>', methods=['GET'])
def delete(id:int):
    sql_operations.deleteTask(taskId=id)
    return redirect(url_for('tasks.index'))