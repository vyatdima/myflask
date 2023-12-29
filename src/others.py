import os
from flask import request, flash, redirect, url_for, render_template, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename
from src import app
from src import logger

app.config['FOLDER_PARENT_STATIC'] = app.name
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder
# print(f'upload_folder={upload_folder}')
# print(f'app.config["FOLDER_PARENT_STATIC"]={app.config["FOLDER_PARENT_STATIC"]}')
make_dir_uploads = os.path.join(app.config['FOLDER_PARENT_STATIC'], upload_folder)
os.makedirs(os.path.abspath(make_dir_uploads), exist_ok=True)

# UPLOAD_FOLDER = 'uploads'
# UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# print(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        upload_folder_save = os.path.join(app.config['FOLDER_PARENT_STATIC'], app.config['UPLOAD'])
        print(upload_folder_save)
        print(os.path.join(upload_folder_save, filename))
        file.save(os.path.join(upload_folder_save, filename))
        path_img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('others/image_render.html', img=path_img)
    return render_template('others/image_render.html')


@app.route('/upload_file_old', methods=['GET', 'POST'])
@login_required
def upload_file_old():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл', 'info')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран', 'info')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'Загружен файл {filename}', 'success')
            logger.info(f'Загружен файл {filename}')
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('others/upload_file.html')


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

#
# config.py
# basedir = os.path.abspath(os.path.dirname(__file__))
# UPLOAD_PATH = os.path.join(basedir, 'audio')
#
# # views.py
# from flask import current_app, send_from_directory
# @main.route('/audio/<path:filename>')
# def audio_dir(filename):
#     return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
#
# # audio.html
# <param name="FlashVars" value="mp3={{ url_for('main.audio_dir', filename=item.name) }}" />



# filename = form.upload.data.filename
# uniquename = uuid.uuid4()
# af = AudioFile(
#     name = uniquename.__str__(),
#     filename = filename
# )
# try:
#     form.upload.data.save(os.path.join(current_app.config['UPLOAD_PATH'], uniquename.__str__()))
#     db.session.add(af)