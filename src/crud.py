from flask import redirect, url_for, request, render_template, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import datetime
import os
import transliterate

from src.forms import UserEditForm
from src.models import Sitefile, Gallery, Page, Organizer, Location, Event, User, db
from src import app


@app.route('/adminka')
@login_required
def adminka():
    if current_user.get_admin():
        return render_template('crud/adminka.html',  title='Админка',)
    flash('У Вас нет доступа к администрированию!', 'danger')
    return redirect(url_for('index'))


@app.route('/sitefiles')
@login_required
def sitefiles():
    return render_template('crud/sitefiles.html', list=Sitefile.query.all())


@app.route('/organizers')
@login_required
def organizers():
    return render_template('crud/organizers.html', list=Organizer.query.all())


@app.route('/pages')
@login_required
def pages():
    return render_template('crud/pages.html', list=Page.query.all())


@app.route('/locations')
@login_required
def locations():
    return render_template('crud/locations.html', list=Location.query.all())


@app.route('/events')
@login_required
def events():
    return render_template('crud/events.html', list=Event.query.order_by(Event.event_date).all())


@app.route('/users')
@login_required
def users():
    return render_template('crud/users.html', list=User.query.order_by(User.is_admin.desc(), User.name).all())


# блок: добавление записей
@app.route('/add_page', methods=['GET', 'POST'])
@login_required
def add_page():
    if request.method == 'POST':
        title = request.form['title']
        name_route = request.form['name_route']
        page_body = request.form['page_body']
        new_record = Page(title=title, name_route=name_route, page_body=page_body)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('pages'))
    return render_template('crud/add_page.html')


@app.route('/add_sitefile', methods=['GET', 'POST'])
@login_required
def add_sitefile():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['filename']
        if file:
            s_filename = transliterate.translit(file.filename, reversed=True)
            s_filename = secure_filename(s_filename)
            upload_folder_save = os.path.join(app.config['FOLDER_PARENT_STATIC'], app.config['UPLOAD'])
            file.save(os.path.join(upload_folder_save, s_filename))
            new_record = Sitefile(title=title, filename=s_filename)
            db.session.add(new_record)
            db.session.commit()
        return redirect(url_for('sitefiles'))
    return render_template('crud/add_sitefile.html')


@app.route('/add_organizer', methods=['GET', 'POST'])
@login_required
def add_organizer():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        file = request.files['img']
        logo = None
        if file:
            s_filename = transliterate.translit(file.filename, reversed=True)
            s_filename = secure_filename(s_filename)
            upload_folder_save = os.path.join(app.config['FOLDER_PARENT_STATIC'], app.config['UPLOAD'])
            file.save(os.path.join(upload_folder_save, s_filename))
            logo = s_filename
        new_record = Organizer(title=title, link=link, logo=logo)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('organizers'))
    return render_template('crud/add_organizer.html')


@app.route('/add_organizer_from_csv', methods=['GET', 'POST'])
@login_required
def add_organizer_from_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        file_data = file.read().decode("windows-1251")
        lines = file_data.split("\n")
        count = 0
        for line in lines:
            row = line.split(";")
            count += 1
            if line.count(';') >= 1 and count > 1:
                title = row[0].strip()
                link = row[1].strip()
                organizer = Organizer.query.filter(Organizer.title == title).first()
                if not organizer:
                    new_record = Organizer(title=title, link=link)
                    db.session.add(new_record)
                    db.session.commit()
                else:
                    organizer.link = link
                    db.session.commit()
        return redirect(url_for('organizers'))
    else:
        return render_template('crud/upload_from_file.html')


@app.route('/add_location', methods=['GET', 'POST'])
@login_required
def add_location():
    if request.method == 'POST':
        title = request.form['title']
        new_record = Location(title=title)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('crud/add_location.html')


@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    location_all = Location.query.all()
    organizer_all = Organizer.query.all()
    if request.method == 'POST':
        title = request.form['title']
        location_id = request.form['location']
        link_geoposition = request.form['link_geoposition']
        organizer_id = request.form['organizer']
        event_date = request.form['event_date']
        event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d')
        len_dist = request.form['len_dist']
        len_dist = float(len_dist.replace(',', '.'))
        time_result = request.form['time_result']
        link_event = request.form['link_event']
        tip_event = request.form['tip_event']
        link_protokol = request.form['link_protokol']
        my_review = request.form['my_review']
        file = request.files['img']
        logo = None
        if file:
            s_filename = transliterate.translit(file.filename, reversed=True)
            s_filename = secure_filename(s_filename)
            upload_folder_save = os.path.join(app.config['FOLDER_PARENT_STATIC'], app.config['UPLOAD'])
            file.save(os.path.join(upload_folder_save, s_filename))
            logo = s_filename
        new_record = Event(title=title, event_date=event_date, len_dist=len_dist, time_result=time_result, link_event=link_event, location_id=location_id, organizer_id=organizer_id, my_review=my_review, logo=logo, tip_event=tip_event, link_protokol=link_protokol, link_geoposition=link_geoposition)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('crud/add_event.html', locations=location_all, organizers=organizer_all)


@app.route('/add_event_from_csv', methods=['GET', 'POST'])
@login_required
def add_event_from_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        file_data = file.read().decode("windows-1251")
        lines = file_data.split("\n")
        count = 0
        for line in lines:
            row = line.split(";")
            count += 1
            if line.count(';') >= 4 and count > 1:

                location_title = row[8].strip()
                location = Location.query.filter(Location.title == location_title).first()
                if not location:
                    new_record = Location(title=location_title)
                    db.session.add(new_record)
                    db.session.commit()
                    location = Location.query.filter(Location.title == location_title).first()
                location_id = location.id

                organizer_title = row[5].strip()
                organizer = Organizer.query.filter(Organizer.title == organizer_title).first()
                if not organizer:
                    new_record = Organizer(title=organizer_title)
                    db.session.add(new_record)
                    db.session.commit()
                    organizer = Organizer.query.filter(Organizer.title == organizer_title).first()
                organizer_id = organizer.id

                title = row[0].strip()
                date_obj = datetime.datetime.strptime(row[1].strip(), '%d.%m.%Y')
                event_date = date_obj.date()
                len_dist = row[2].strip()
                len_dist = float(len_dist.replace(',', '.'))
                time_result = row[3].strip()
                link_event = row[4].strip()
                tip_event = row[7].strip()
                link_protokol = row[9].strip()
                link_geoposition = row[10].strip()
                event = Event.query.filter(Event.title == title, Event.event_date == event_date).first()
                if not event:
                    new_record = Event(title=title, event_date=event_date, len_dist=len_dist, time_result=time_result, link_event=link_event, location_id=location_id, organizer_id=organizer_id, tip_event=tip_event, link_protokol=link_protokol, link_geoposition=link_geoposition)
                    db.session.add(new_record)
                    db.session.commit()
                else:
                    event.len_dist = len_dist
                    event.time_result = time_result
                    event.link_event = link_event
                    event.location_id = location_id
                    event.organizer_id = organizer_id
                    event.tip_event = tip_event
                    event.link_protokol = link_protokol
                    event.link_geoposition = link_geoposition
                    db.session.commit()
        return redirect(url_for('events'))
    else:
        return render_template('crud/upload_from_file.html')


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['confirmPassword']
        new_record = User(name=name, password=password, email=email)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('crud/add_user.html')


@app.route('/edit_page/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_page(id):
    page = Page.query.get_or_404(id)
    if request.method == 'POST':
        page.title = request.form['title']
        page.name_route = request.form['name_route']
        page.page_body = request.form['page_body']
        db.session.commit()
        return redirect(url_for('pages'))
    return render_template('crud/edit_page.html', page=page)


@app.route('/edit_sitefile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sitefile(id):
    sitefile = Sitefile.query.get_or_404(id)
    if request.method == 'POST':
        sitefile.title = request.form['title']
        db.session.commit()
        return redirect(url_for('sitefiles'))
    return render_template('crud/edit_sitefile.html', sitefile=sitefile)


@app.route('/edit_organizer/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_organizer(id):
    organizer = Organizer.query.get_or_404(id)
    if request.method == 'POST':
        organizer.title = request.form['title']
        organizer.link = request.form['link']
        delete_logo = request.form['delete_logo'] if request.form.get('delete_logo') else None
        file = request.files['img']
        if file:
            s_filename = transliterate.translit(file.filename, reversed=True)
            s_filename = secure_filename(s_filename)
            upload_folder_save = os.path.join(app.config['FOLDER_PARENT_STATIC'], app.config['UPLOAD'])
            file.save(os.path.join(upload_folder_save, s_filename))
            organizer.logo = s_filename
        if delete_logo == 'on':
            organizer.logo = None
        db.session.commit()
        return redirect(url_for('organizers'))
    return render_template('crud/edit_organizer.html', organizer=organizer)


@app.route('/edit_location/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_location(id):
    location = Location.query.get_or_404(id)
    if request.method == 'POST':
        location.title = request.form['title']
        db.session.commit()
        return redirect(url_for('locations'))
    return render_template('crud/edit_location.html', location=location)


@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    location_all = Location.query.all()
    organizer_all = Organizer.query.all()
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.tip_event = request.form['tip_event']
        event_date = request.form['event_date']
        event.event_date = datetime.datetime.strptime(event_date, '%Y-%m-%d')
        event.location_id = request.form['location']
        event.link_geoposition = request.form['link_geoposition']
        event.organizer_id = request.form['organizer']
        len_dist = request.form['len_dist']
        event.len_dist = float(len_dist.replace(',', '.'))
        event.time_result = request.form['time_result']
        event.link_event = request.form['link_event']
        event.link_protokol = request.form['link_protokol']
        event.my_review = request.form['my_review']
        delete_logo = request.form['delete_logo'] if request.form.get('delete_logo') else None
        file = request.files['img']
        if file:
            s_filename = transliterate.translit(file.filename, reversed=True)
            s_filename = secure_filename(s_filename)
            upload_folder_save = os.path.join(app.config['FOLDER_PARENT_STATIC'], app.config['UPLOAD'])
            file.save(os.path.join(upload_folder_save, s_filename))
            event.logo = s_filename
        if delete_logo == 'on':
            event.logo = None
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('crud/edit_event.html', event=event, locations=location_all, organizers=organizer_all)


# @app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_user(id):
#     form = UserEditForm(request.form)
#     user = User.query.get_or_404(id)
#     form.is_admin.data = user.is_admin
#     form.name.data = user.name
#     form.email.data = user.email
#     form.password.data = user.password
#     print(user.password)
#     if request.method == 'POST':
#         if form.validate():
#             print(form.is_admin.data)
#             is_admin = form.is_admin.data if form.is_admin.data else False
#             user.is_admin = True if is_admin == 'on' else False
#             user.name = form.name.data
#             user.email = form.email.data
#             user.password = form.password.data
#             db.session.commit()
#             return redirect(url_for('users'))
#         else:
#             print('не свалидировано')
#     return render_template('crud/form_edit_user.html', form=form, user=user)


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        is_admin = request.form['is_admin'] if request.form.get('is_admin') else False
        user.is_admin = True if is_admin == 'on' else False
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('crud/edit_user.html', user=user)


@app.route('/del_page/<int:id>', methods=['POST'])
@login_required
def del_page(id):
    page = Page.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(page)
        db.session.commit()
        return redirect(url_for('pages'))


@app.route('/del_sitefile/<int:id>', methods=['POST'])
@login_required
def del_sitefile(id):
    sitefile = Sitefile.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(sitefile)
        db.session.commit()
        return redirect(url_for('sitefiles'))


@app.route('/del_organizer/<int:id>', methods=['POST'])
@login_required
def del_organizer(id):
    organizer = Organizer.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(organizer)
        db.session.commit()
        return redirect(url_for('organizers'))


@app.route('/del_location/<int:id>', methods=['POST'])
@login_required
def del_location(id):
    location = Location.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(location)
        db.session.commit()
        return redirect(url_for('locations'))


@app.route('/del_event/<int:id>', methods=['POST'])
@login_required
def del_event(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('events'))


@app.route('/del_user/<int:id>', methods=['POST'])
@login_required
def del_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users'))
