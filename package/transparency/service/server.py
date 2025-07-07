from transparency.card import ModelCard
from transparency.service.assistant import Assistant
from flask import Flask, jsonify, request, abort, redirect
from threading import Lock, Thread


def exists(condition, message):
    # empty strings are allowed
    if condition is not None and isinstance(condition, str): return condition
    if not condition: abort(404, description=message)
    return condition

class ModelCardEntry:
    def __init__(self, card: ModelCard):
        self.card = card
        self.lock = Lock()
        self.__is_completing = False
        self.__thread = None

    def start_completion(self):
        self.lock.acquire_lock()
        if self.__is_completing:
            self.lock.release_lock()
            abort(409, description="The AI assistant is working on the model card")
        self.__is_completing = True
        self.lock.release_lock()

    def check_completion(self):
        self.lock.acquire_lock()
        ret = self.__is_completing
        self.lock.release_lock()
        return ret

    def end_completion(self):
        self.lock.acquire_lock()
        self.__is_completing = False
        self.lock.release_lock()

    def __enter__(self):
        self.lock.acquire_lock()
        if self.__is_completing:
            self.lock.release_lock()
            abort(409, description="The AI assistant is working on the model card")
        return self.card

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release_lock()

    def __autocomplete(self, url: str, assistant: Assistant):
        assistant.complete(self.card, url)
        self.end_completion()

    def __autorefine(self, assistant: Assistant):
        assistant.refine(self.card)
        self.end_completion()

    def autocomplete(self, url: str, assistant: Assistant):
        self.start_completion()
        self.__thread = Thread(target=self.__autocomplete, args=(url,assistant))
        self.__thread.start()
        return "submitted"

    def autorefine(self, assistant: Assistant):
        self.start_completion()
        self.__thread = Thread(target=self.__autocomplete, args=(assistant,))
        self.__thread.start()
        return "submitted"

    def get_status(self):
        if self.check_completion(): return {"status": "locked", "message": "AI assistant is working on the model card"}
        return {"status": "editable", "message": "You can edit the model card"}



def serve(redirect_index, assistants: dict[str, Assistant]):
    app = Flask(__name__)
    test_data: dict[int, ModelCardEntry | None] = dict()

    @app.route("/", methods=['GET'])
    def get_index():
        return redirect(redirect_index, code=307)

    @app.route('/cards', methods=['GET'])
    def get_cards():
        return jsonify([key for key, value in test_data.items() if value is not None])

    @app.route('/assistants', methods=['GET'])
    def get_assistants():
        return jsonify({key: value.description for key, value in assistants.items()})

    @app.route('/card/<int:card_id>', methods=['GET'])
    def get_card(card_id):
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            return jsonify(card.data)

    @app.route('/card/<int:card_id>/title', methods=['GET', 'POST'])
    def card_title(card_id):
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            if request.method == 'GET': return jsonify(card.title)
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card titles.")
            card.data['title'] = json_data
            return jsonify(card.data['title'])  # do not return json_data directly, as setting the value may format it

    @app.route('/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['GET', 'POST'])
    def card_field(card_id, field_name, data_name):
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            if request.method == 'GET': return jsonify(data)
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card fields.")
            field[data_name] = json_data
            return jsonify(field[data_name])  # do not return json_data directly, as setting the value may format it

    @app.route('/card/<int:card_id>', methods=['DELETE'])
    def delete_card(card_id):
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as _:
            test_data[card_id] = None
            return '', 204

    @app.route('/card/<int:card_id>', methods=['POST'])
    def update_card(card_id):
        json_data = request.get_json()
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            card.data.assign(json_data)
            return jsonify(card.data)

    @app.route('/card', methods=['POST'])
    def create_card():
        json_data = request.get_json()
        card = ModelCardEntry(ModelCard())
        if json_data:
            try:
                card.card.data.assign(json_data)
            except AssertionError as e:
                print("Assertion error: "+str(e))
                abort(500, description=str(e))
            except Exception as e:
                print("Exception: "+str(e))
                abort(500, description=str(e))
        card_id = len(test_data)
        test_data[card_id] = card
        return jsonify(card_id)

    @app.route('/assistant/<string:assistant_type>/complete/<int:card_id>', methods=['POST'])
    def autocomplete_card(card_id: int, assistant_type: str):
        json_data = request.get_json()
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        exists(isinstance(json_data, str), "Autocomplete requires a url string as POST data")
        status = exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.").autocomplete(json_data, assistant)
        return jsonify(status)

    @app.route('/assistant/<string:assistant_type>/refine/<int:card_id>', methods=['GET'])
    def autorefine_card(card_id: int, assistant_type: str):
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        status = exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.").autorefine(assistant)
        return jsonify(status)

    @app.route('/docs', methods=['GET'])
    def docs():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':  continue
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            routes.append({
                "endpoint": rule.endpoint,
                "methods": methods,
                "path": str(rule),
            })
        return jsonify(routes)

    return app
