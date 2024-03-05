import model


class StorageException(Exception):
    pass


class LocalStorage:
    def __init__(self):
        self._id_counter = 0
        self._storage = {}

    def create_event(self, event: model.Event):
        self._id_counter += 1
        event.id = str(self._id_counter)
        self._storage[event.id] = event
        return event.id

    def list_events(self):
        return list(self._storage.values())

    def read_event(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"_id not found in storage")
        return self._storage[_id]

    def update_event(self, _id: str, event: model.Event):
        if _id not in self._storage:
            raise StorageException(f"_id not found in storage")
        event.id = _id
        self._storage[event.id] = event

    def delete_event(self, _id: str):
        if _id not in self._storage:
            raise StorageException(f"_id not found in storage")
        del self._storage[_id]
