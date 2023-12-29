from datetime import datetime
from flask import render_template, redirect, url_for
from sqlalchemy.sql import func

from src.models import Sitefile, Gallery, Page, Organizer, Event, User
from src import app


@app.route('/')
def index():
    contex = {
        'list_events_new': Event.query.order_by(Event.event_date).filter(Event.event_date >= datetime.now()),
        'list_events_old': Event.query.order_by(Event.event_date.desc()).filter(Event.event_date < datetime.now()),
        'list_users': User.query.order_by(User.is_admin.desc(), User.name).all(),
        'list_organizers': Organizer.query.order_by(Organizer.title).all(),
        'slider_index': Sitefile.query.order_by(func.random()).all(),
    }
    return render_template('index.html', **contex)


@app.route('/page/<name_route>')
def view_page(name_route):
    page = Page.query.filter(Page.name_route == name_route).first()
    if page:
        return render_template('view_page.html', page=page)
    return redirect(url_for('index'))


# @app.route('/about')
# def about():
#     return render_template('about.html')


@app.route('/event/<int:event_id>')
def event(event_id):
    return render_template('event.html', event=Event.query.get_or_404(event_id))


def def_minus(par1):
    return par1 - 1


@app.template_filter('minus_1')
def t_minus_1(s):
    return s - 1
