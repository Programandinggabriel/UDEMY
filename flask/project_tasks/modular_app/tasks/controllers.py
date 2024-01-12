import os

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required

from modular_app.tasks import models, sql_operations, forms
from modular_app.documents import sql_operations as doc_sql_operations

from modular_app import app
from modular_app import config

from werkzeug.utils import secure_filename

taskRoute = Blueprint('tasks', __name__, url_prefix='/tasks')

@taskRoute.before_request
@login_required
def before():
    pass

@taskRoute.route('/')
def index():
    aTasks = sql_operations.getAllTask()
    return render_template('dashboard/task/index.html', tasks = aTasks)

@taskRoute.route('/create', methods=['POST', 'GET'])
def create():
    frm = forms.TaskForm()

    #Agrego opciones a el elemento SELECT
    frm.category.choices = [(row.id, row.name) for row in models.Category.query.all()]

    if frm.validate_on_submit():
        sql_operations.createTask(frm.name.data, frm.category.data)

        return redirect(url_for('tasks.index'))
        #print(request.args.get('task'))

    return render_template('dashboard/task/create.html', form=frm)

@taskRoute.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id:int):
    oTask = sql_operations.getTaskById(id)
    
    frm = forms.TaskForm()    
    frm.category.choices = [(row.id, row.name)for row in models.Category.query.all()]
    frm.category.data = str(oTask.category.id)

    #Tags
    #Add
    frmTag = forms.TaskAddTagForm()
    frmTag.tag.choices = [(row.id, row.name)for row in models.Tag.query.all()]
    #Remove
    frmTagRem = forms.TaskDeleteTagForm()

    if request.method == 'GET':        
        frm.name.data = oTask.name
    elif request.method == 'POST':
        if frm.validate_on_submit():            
            #Valida archivo cargado
            oFileStorage = frm.file.data

            if oFileStorage and config.validate_ext_file(filename=oFileStorage.filename):
                fileName = secure_filename(oFileStorage.filename)
                oFileStorage.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))

                oDocument = doc_sql_operations.createDocument(filename=fileName)
                #actualiza task con el respectivo id del document creado
                sql_operations.updateTask(taskId=id, taskName=frm.name.data, documentId=oDocument.id, categoryID=oTask.category.id)

                flash(message='Registro actualizado correctamente') 

            #return redirect(url_for('tasks.index'))
    
    return render_template('dashboard/task/update.html', form=frm, frmTag=frmTag, frmTagRem=frmTagRem,id=oTask.id, task=oTask)

@taskRoute.route('/delete/<int:id>', methods=['GET'])
def delete(id:int):
    oTask = sql_operations.getTaskById(id)
    
    sql_operations.deleteTask(taskId=oTask.id)
    doc_sql_operations.deleteDocument(oTask.document_id)
    
    filename = oTask.document.name
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('tasks.index'))

#Tag
@taskRoute.route('/<int:id>/tag/add', methods=['POST'])
def addTag(id:int):
    formTag = forms.TaskAddTagForm()
    formTag.tag.choices = [(row.id, row.name)for row in models.Tag.query.all()]

    if(formTag.validate_on_submit()):
        sql_operations.addTagTask(taskId=id, tagId=formTag.tag.data)

    return redirect(url_for('tasks.update', id=id))

@taskRoute.route('/<int:id>/tag/remove', methods=['POST'])
def deleteTag(id:int):
    frmTagRem = forms.TaskDeleteTagForm()
    tagId = frmTagRem.tag.data

    if(frmTagRem.validate_on_submit()):
        sql_operations.removeTagTask(taskId=id, tagId=tagId)

    return redirect(url_for('tasks.update', id=id))