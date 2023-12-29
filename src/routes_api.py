import datetime
from datetime import date
from flask import request
from flask_restful import Resource

from src import api, db
from src.models import Event


class Smoke(Resource):
    def get(self):
        return {'message': 'OK'}


class EventListApi(Resource):
    def get(self, id=None):
        if not id:
            events = db.session.query(Event).all()
            retval = [f.to_dict() for f in events]
            return retval, 200
        event = db.session.query(Event).filter_by(id=id).first()
        if not event:
            retval = ""
            return retval, 404
        retval = event.to_dict()
        return retval, 200

    def post(self):
        event_json = request.json
        print(f'event_json:{event_json}')
        if not event_json:
            return {'message': 'Нет данных'}, 400
        try:
            event = Event(
                title=event_json['title'],
                event_date=datetime.datetime.strptime(event_json['event_date'], '%d.%m.%Y'),
            )
            db.session.add(event)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Успешное добавление данных', 'id': event.id}, 201

    def put(self, id):
        event_json = request.json
        print(f'event_json:{event_json}')
        if not event_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Event).filter_by(id=id).update(
                dict(
                    title=event_json['title'],
                    event_date=datetime.datetime.strptime(event_json['event_date'], '%d.%m.%Y'),
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Успешное обновление данных'}, 200


    def patch(self, id):
        event = db.session.query(Event).filter_by(id=id).first()
        if not event:
            return "", 404
        event_json = request.json
        print(f'event_json:{event_json}')
        title = event_json.get('title')
        event_date = datetime.datetime.strptime(event_json.get('event_date'), '%d.%m.%Y') if event_json.get(
            'event_date') else None
        if title:
            event.title = title
        elif event_date:
            event.event_date = event_date

        db.session.add(event)
        db.session.commit()
        return {'message': 'Updated successfully'}, 200


    def delete(self, id):
        event = db.session.query(Event).filter_by(id=id).first()
        if not event:
            return "", 404
        db.session.delete(event)
        db.session.commit()
        return '', 204


api.add_resource(Smoke, '/', strict_slashes=False)
api.add_resource(EventListApi, '/events', '/events/<id>', strict_slashes=False)

