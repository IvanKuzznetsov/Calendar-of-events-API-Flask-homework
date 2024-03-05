import model
import db
from datetime import date


TITLE_LIMIT = 30
TEXT_LIMIT = 200


class LogicException(Exception):
    pass


class EventLogic:
    def __init__(self):
        self._event_db = db.EventDB()

    @staticmethod
    def _validate_event(event: model.Event):
        if event is None:
            raise LogicException("note is None")
        if event.title is None or len(event.title) > TITLE_LIMIT:
            raise LogicException(f"title lenght > MAX: {TITLE_LIMIT}")
        if event.text is None or len(event.text) > TITLE_LIMIT:
            raise LogicException(f"text lenght > MAX: {TEXT_LIMIT}")
        _date = str(event.date)
        splited_date = _date.split("-")
        try:
            date(int(splited_date[0]), int(splited_date[1]), int(splited_date[2]))
        except Exception:
            raise LogicException('invalid date')

    def _check_date(self, event: model.Event):
        events = self._event_db.list_events()
        for i in events:
            if i.date == event.date:
                raise LogicException("An event already exists on this day. You can add only one event per day.")

    def create_event(self, event: model.Event):
        self._validate_event(event)
        self._check_date(event)
        try:
            return self._event_db.create_event(event)
        except Exception as ex:
            raise LogicException(f"failed to CREATE with: {ex}")

    def list_events(self):
        try:
            return self._event_db.list_events()
        except Exception as ex:
            raise LogicException(f"failed to LIST with: {ex}")

    def read_event(self, _id: str):
        try:
            return self._event_db.read_event(_id)
        except Exception as ex:
            raise LogicException(f"failed to READ with: {ex}")

    def update_event(self, _id: str, event: model.Event):
        self._validate_event(event)
        try:
            return self._event_db.update_event(_id, event)
        except Exception as ex:
            raise LogicException(f"failed to UPDATE with: {ex}")

    def delete_event(self, _id: str):
        try:
            return self._event_db.delete_event(_id)
        except Exception as ex:
            raise LogicException(f"failed to DELETE with: {ex}")
