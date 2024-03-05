from flask import Flask, request, jsonify

import model
import logic


app = Flask(__name__)

_event_logic = logic.EventLogic()


class ApiException(Exception):
    pass


def _from_raw(raw_event):
    try:
        event = model.Event()
        event.date = raw_event["date"]
        event.title = raw_event["title"]
        event.text = raw_event["text"]
        return event
    except Exception:
        raise ApiException(f"invalid RAW event data {raw_event}")


def to_dict(event: model.Event):
    try:
        return {"id": event.id, "date": event.date, "title": event.title, "text": event.text}
    except Exception as ex:
        raise ApiException(f"invalid event data: {ex}")


API_ROOT = "/api/v1"
EVENT_API_ROOT = API_ROOT + "/calendar"


@app.route(EVENT_API_ROOT + "/", methods=['POST'])
def create_event():
    try:
        event_json = request.get_json()
        event = _from_raw(event_json)
        _id = _event_logic.create_event(event)
        return jsonify({'new id': f'{str(_id)}'}), 201
    except Exception as ex:
        return jsonify({'failed to CREATE with': f'{ex}'}), 404


@app.route(EVENT_API_ROOT + "/", methods=['GET'])
def list_events():
    try:
        events = _event_logic.list_events()
        serialised_events = []
        for event in events:
            serialised_events.append(to_dict(event))
        return jsonify({"events": serialised_events}), 200
    except Exception as ex:
        return jsonify({'failed to LIST with': f'{ex}'}), 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=['GET'])
def read_event(_id: str):
    try:
        event = _event_logic.read_event(_id)
        event_dict = to_dict(event)
        return jsonify(event_dict), 200
    except Exception as ex:
        return jsonify({'failed to READ with': f'{ex}'}), 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=['PUT'])
def update_event(_id: str):
    try:
        event_json = request.get_json()
        event = _from_raw(event_json)
        _event_logic.update_event(_id, event)
        return jsonify({"status": "updated"}), 200
    except Exception as ex:
        return jsonify({'failed to UPDATE with': f'{ex}'}), 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=['DELETE'])
def delete_event(_id: str):
    try:
        _event_logic.delete_event(_id)
        return jsonify({"status": "deleted"}), 200
    except Exception as ex:
        return jsonify({'failed to DELETE with': f'{ex}'}), 404
