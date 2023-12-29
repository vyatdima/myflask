import jwt
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from time import time
import jwt
db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "site_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(1000), index=True, unique=True)
    fam = db.Column(db.String(128))
    nam = db.Column(db.String(128))
    password = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    def get_admin(self):
        if self.is_admin:
            return True
        else:
            return False

    def set_password(self, cdata):
        self.password = cdata
        return ''

    def get_reset_password_token(self, expires_in=600):
        aaa = {'reset_password': self.id, 'exp': time() + expires_in}
        bbb = jwt.encode(aaa, 'gfggdgfhgjkujyytyty', algorithm='HS256')
        return bbb

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, 'gfggdgfhgjkujyytyty', algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f'{self.name}'


class Organizer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    link = db.Column(db.String(120))
    logo = db.Column(db.String(120))


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(120), nullable=False)
    tip_event = db.Column(db.String(120))
    link_geoposition = db.Column(db.String(120))
    logo = db.Column(db.String(120))
    event_date = db.Column(db.Date)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    location = db.relationship('Location', backref=db.backref('events', lazy=True))
    len_dist = db.Column(db.Float())
    time_result = db.Column(db.String(15))
    link_event = db.Column(db.String(120))
    link_protokol = db.Column(db.String(120))
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.id'), nullable=True)
    organizer = db.relationship('Organizer', backref=db.backref('organizers', lazy=True))
    my_review = db.Column(db.Text)


    def __repr__(self):
        date_to_german = self.event_date.strftime('%d.%m.%Y')
        return f'Event({date_to_german} {self.title})'

    def to_dict(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'title': self.title,
            'event_date': self.event_date.strftime('%d.%m.%Y') if self.event_date else None,
            'location_id': self.location_id,
            'organizer_id': self.organizer_id,
            'len_dist': self.len_dist,
            'time_result': self.time_result,
            'link_event': self.link_event,
            'my_review': self.my_review,
        }


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(120), nullable=False)
    name_route = db.Column(db.String(120), nullable=False)
    page_body = db.Column(db.Text)


class Sitefile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(120))
    title = db.Column(db.String(120), nullable=False)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('sitefile.id'), nullable=True)
    sitefile = db.relationship('Sitefile', backref=db.backref('sitefiles', lazy=True))
