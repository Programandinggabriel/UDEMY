from flask import Blueprint, render_template, request, redirect, url_for
from modular_app.tasks import sql_operations

taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

@taskRoute.route('/')
def index():
    aTasks = sql_operations.getAllTask()
    return render_template('dashboard/task/index.html', tasks = aTasks)

@taskRoute.route('/create', methods=['POST', 'GET'])
def create():
    sTask = request.form.get('task')
    
    if sTask is not None:
     sql_operations.createTask(sTask)

     return redirect(url_for('tasks.index'))
    #print(request.args.get('task'))

    return render_template('dashboard/task/create.html')

@taskRoute.route('/<int:id>', methods=['GET'])
def show(id:int):
    task = sql_operations.getTaskById(taskId=id)

    return 'Mostrando task ' + task.name

@taskRoute.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id:int):
    sTaskName = request.form.get('task')

    if sTaskName is not None:
     sql_operations.updateTask(taskId=id, taskName=sTaskName)
     
     return redirect(url_for('tasks.index'))
    
    return render_template('dashboard/task/update.html')

@taskRoute.route('/delete/<int:id>', methods=['GET'])
def delete(id:int):
    sql_operations.deleteTask(taskId=id)
    return redirect(url_for('tasks.index'))