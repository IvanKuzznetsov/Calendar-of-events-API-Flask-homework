import model
import storage


class DBException(Exception):
    pass


class EventDB:
    def __init__(self):
        self._storage = storage.LocalStorage()

    def create_event(self, event: model.Event):
        try:
            return self._storage.create_event(event)
        except Exception as ex:
            raise DBException(f"failed to CREATE with: {ex}")

    def list_events(self):
        try:
            return self._storage.list_events()
        except Exception as ex:
            raise DBException(f"failed to LIST with: {ex}")

    def read_event(self, _id: str):
        try:
            return self._storage.read_event(_id)
        except Exception as ex:
            raise DBException(f"failed to READ with: {ex}")

    def update_event(self, _id: str, event: model.Event):
        try:
            return self._storage.update_event(_id, event)
        except Exception as ex:
            raise DBException(f"failed to UPDATE with: {ex}")

    def delete_event(self, _id: str):
        try:
            return self._storage.delete_event(_id)
        except Exception as ex:
            raise DBException(f"failed to DELETE with: {ex}")
