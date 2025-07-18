from modelcard.card import ModelCard
from modelcard.service.assistant import Assistant
from flask import Flask, jsonify, request, abort, redirect
from flasgger import Swagger
from threading import Lock, Thread
from flask import request, jsonify

def dynamic2dict(data, mixed: set=None):
    if mixed:
        if not isinstance(data, dict): return dynamic2dict(data)
        if "data" not in data: return dynamic2dict(data)
        for mix in mixed: assert mix in data, f"No {mix} key dictionary key found"
        data_segment = dynamic2dict(data["data"])
        assert isinstance(data_segment, dict), "Data segment could not be parsed into a dictionary"
        return {mix: data[mix] for mix in mixed}|data_segment
    if isinstance(data, list) and all(isinstance(item, dict) and len(item)==2 and "name" in item and "value" in item for item in data):
        return {item["name"]: dynamic2dict(item["value"]) for item in data}
    return data

def dict2dynamic(data, mixed: set=None):
    if mixed:
        assert isinstance(data, dict)
        for mix in mixed: assert mix in data
        return {mix: data[mix] for mix in mixed}|{"data": dict2dynamic({k: v for k, v in data.items() if k not in mixed})}
    if isinstance(data, dict): return [{"name": k, "value": dict2dynamic(v)} for k, v in data.items()]
    return data

def exists(condition, message):
    # empty strings are allowed
    if condition is not None and isinstance(condition, str): return condition
    if not condition: abort(404, description=message)
    return condition

class ModelCardEntry:
    def __init__(self, card: ModelCard):
        self.card = card
        self.preview = card.to_html_card()
        self.lock = Lock()
        self.__is_completing = False
        self.__thread = None

    def start_completion(self):
        self.lock.acquire()
        if self.__is_completing:
            self.lock.release()
            abort(409, description="An AI assistant is working on the model card")
        self.__is_completing = True
        self.lock.release()

    def check_completion(self):
        self.lock.acquire()
        ret = self.__is_completing
        self.lock.release()
        return ret

    def end_completion(self):
        self.lock.acquire()
        self.__is_completing = False
        self.lock.release()

    def __enter__(self):
        self.lock.acquire()
        if self.__is_completing:
            self.lock.release()
            abort(409, description="An AI assistant is working on the model card")
        return self.card

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

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
        self.__thread = Thread(target=self.__autorefine, args=(assistant,))
        self.__thread.start()
        return "submitted"

    def get_status(self):
        if self.check_completion(): return {"status": "locked", "message": "AI assistant is working on the model card"}
        return {"status": "editable", "message": "You can edit the model card"}



def serve(redirect_index, assistants: dict[str, Assistant]):
    app = Flask(__name__)
    empty_card = ModelCard()
    swagger = Swagger(app, template = {
        "swagger": "2.0",
        "info": {"title": "ModelCard",
            "description": "API docs",
            "version": "0.0.2"
        }
    })
    test_data: dict[int, ModelCardEntry | None] = dict()

    @app.route("/", methods=['GET'])
    def get_index():
        return redirect(redirect_index, code=307)

    @app.route('/cards', methods=['POST'])
    def get_cards():
        """
        Retrieves a list of model cards while filtering for a search query and performing pagination.
        The results contain both card id, title and descriptions, and the total number of pages
        for the particular pagination limit. If no query is provided, all cards will be considered.
        If no page size is provided, or if non-positive, 10 is assumed. If no page is provided,
        or if it's non-positive, 1 (the first page) is assumed.
        ---
        tags:
          - UI
        parameters:
          - name: query
            in: body
            type: string
            required: false
            description: Case-insensitive filter on card titles or contents.
            example: "my card"
          - name: page
            in: body
            type: integer
            required: false
            default: 1
            description: Page number, starting from 1.
          - name: page_size
            in: body
            type: integer
            required: false
            default: 10
            description: Number of results per page.
        responses:
          200:
            description: A paginated list of card summaries.
            schema:
              type: object
              properties:
                results:
                  type: array
                  description: List of card summaries.
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: Card identifier.
                      name:
                        type: string
                        description: Card title.
                      desc:
                        type: string
                        description: Card description. For now, this is a brief note on completion percentage, but will become a summary line in the future.
                pages:
                  type: integer
                  description: Total number of result pages.
        """

        data = request.get_json() or {}
        query = data.get('query', '').strip().lower()
        page = int(data.get('page', 1))
        page_size = int(data.get('page_size', 10))
        if page < 1: page = 1
        if page_size < 1: page_size = 10
        filtered = [
            {
                "id": key,
                "name": value.card.title,
                "desc": f"Completion {int(value.card.quality() * 100 + 0.5)}%"
            }
            for key, value in test_data.items()
            if value is not None and (not query or query in value.card.title.lower())
        ]
        total = len(filtered)
        num_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = min(start + page_size, total)
        results = filtered[start:end] if start < total else []
        return jsonify({"results": results, "pages": num_pages})

    @app.route('/assistants', methods=['GET'])
    def get_assistants():
        """
        Retrieves all available AI assistants for the current user and card, including their names and descriptions.
        ---
        tags:
          - UI
        responses:
            200:
                description: A list of assistants with their names and descriptions.
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                        description: The name of the assistant.
                      desc:
                        type: string
                        description: The description of the assistant.
        """
        return jsonify([{"name": key, "desc": value.description} for key, value in assistants.items()])

    @app.route('/card/<int:card_id>', methods=['GET'])
    def get_card(card_id):
        """
        Retrieves the JSON data for a given model card.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The unique identifier for the model card.
        responses:
            200:
                description: The JSON representation of the model card.
                schema:
                  type: object
                  description: The model card contents. This includes fields title and a list of related card ids and names.
            404:
                description: The requested card does not exist or has been deleted.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            return jsonify(dict2dynamic(card.data|{"related": []}, {"title"}))

    @app.route('/card/<int:card_id>/locked', methods=['GET'])
    def get_card_locked_status(card_id):
        """
        Retrieves a boolean value of whether the card is locked by an AI assistant working on it.
        If it is locked, post or put methods on the card will create errors.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's unique identifier.
        responses:
            200:
                description: The title of the model card.
                schema:
                  type: string
            404:
                description: The requested card does not exist or has been deleted.
        """
        card = exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.")
        return jsonify(card.check_completion)

    @app.route('/card/<int:card_id>/title', methods=['GET'])
    def get_card_title(card_id):
        """
        Retrieves the title of the specified model card.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's unique identifier.
        responses:
            200:
                description: The title of the model card.
                schema:
                  type: string
            404:
                description: The requested card does not exist or has been deleted.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            return jsonify(card.title)

    @app.route('/card/<int:card_id>/title', methods=['PUT'])
    def set_card_title(card_id):
        """
        Updates the title of the specified model card.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's unique identifier.
          - name: body
            in: body
            required: true
            schema:
              type: string
              example: "New model card title"
        responses:
            200:
                description: The updated title of the model card.
                schema:
                  type: string
            404:
                description: The requested card does not exist or has been deleted, or invalid request body.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card titles.")
            card.data['title'] = json_data
            return jsonify(card.data['title'])

    @app.route('/card/fields', methods=['GET'])
    def get_card_fields():
        """
        Lists all top-level field names for model cards that contain data entries.
        For example, this list does not contain the title but that it contains test datasets, training datasets, etc.
        This method helps the frontend be generalize-able in case there is a need for extensibility.
        Once fields are obtained, use /card/fields/<field_name> to retrieve its data entries.
        ---
        responses:
            200:
                description: List of top-level card field names.
                schema:
                    type: array
                    items:
                        type: string
        """
        return jsonify([key for key, value in empty_card.data.items() if isinstance(value, dict)])

    @app.route('/card/fields/<string:field_name>', methods=['GET'])
    def get_card_field_names(field_name):
        """
        Lists all data entry  names under the given field_name in a model card.
        ---
        parameters:
          - name: field_name
            in: path
            type: string
            required: true
            description: The top-level field name.
        responses:
            200:
                description: List of subfield names for the field.
                schema:
                    type: array
                    items:
                        type: string
            404:
                description: Field does not exist.
        """
        fields = empty_card.data
        field = exists(fields.get(field_name, None), f"Field '{field_name}' does not exist.")
        exists(isinstance(field, dict), f"Field '{field_name}' does not have data entries.")
        return jsonify(list(field.keys()))

    @app.route('/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['GET'])
    def get_card_field(card_id, field_name, data_name):
        """
        Retrieves an entry from card.field_name.data_name.
        For example, retrieve card.model.version.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: field_name
            in: path
            type: string
            required: true
            description: The card's field name. To see all field names available for cards get /card/fields.
          - name: data_name
            in: path
            type: string
            required: true
            description: The data entry name within the card's field To see all data entries available for the field get /card/fields/field_name.
        responses:
            200:
                description: A string containing an editable (markdown) version of data values.
                schema:
                  type: string
                  description: The card's editable string representation.
            404:
                description: Resource does not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            return jsonify(data)

    @app.route('/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['PUT'])
    def set_card_field(card_id, field_name, data_name):
        """
        Sets an value to card.field_name.data_name.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: field_name
            in: path
            type: string
            required: true
            description: The card's field name. To see all field names available for cards get /card/fields.
          - name: data_name
            in: path
            type: string
            required: true
            description: The data entry name within the card's field To see all data entries available for the field get /card/fields/field_name.
          - name: body
            in: body
            required: true
            description: A string to set as value.
            schema:
              type: string
        responses:
            200:
                description: A list of integer identifiers.
                schema:
                    type: array
                    items:
                        type: integer
            404:
                description: Resource does not exist, or invalid body.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card fields.")
            field[data_name] = json_data
            return jsonify(field[data_name])  # do not return json_data directly, as setting the value may format it


    @app.route('/card/<int:card_id>', methods=['DELETE'])
    def delete_card(card_id):
        """
        Removes the respective card; it will be considered a missing resource from now on.
        ---
        tags:
          - UI
        responses:
            204:
                description: Successfully removed.
            404:
                description: Resource does not exist.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as _:
            test_data[card_id] = None
            return '', 204

    @app.route('/card/<int:card_id>', methods=['PUT'])
    def update_card(card_id):
        """
        Updates a model card's contents - enables manual upload.
        The provided json data should be (parts of) a model card's
        json representation with potentially some missing fields, and updates everything in the
        target card. The card's contents after setting everything are returned. This operation
        is safe in that all fields should be valid in order for any to be set.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: body
            in: body
            required: true
            description: Partial or full model card JSON to update the card with. This can be either in the dynamic format used by this API or in a static format that is exported by the modelcard library.
            schema:
              type: object
        responses:
            200:
                description: Successfully set everything and retrieves a json representation of the model card.
            404:
                description: Either the card or at least one of the provided fields do not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        json_data = request.get_json()
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            try: card.data.assign(dynamic2dict(json_data, {"title"}))
            except AssertionError as e: abort(404, "Wrong data: "+str(e))
            except Exception as e: abort(404, "Wrong data: "+str(e))
            return jsonify(dict2dynamic(card.data, {"title"}))

    @app.route('/card', methods=['POST'])
    def create_card():
        """
        Creates a model card given an optional json representation - the representation is for manual upload.
        The provided json data should be either an empty dict or (parts of) a model card's
        json representation with potentially some missing fields, and updates everything in the
        target card. The card's contents after setting everything are retrieved.
        ---
        tags:
          - UI
        parameters:
          - name: body
            in: body
            required: false
            schema:
              type: object
              description: Partial or full model card JSON to update the card with.
        responses:
            200:
                description: Successfully set everything and retrieves a json representation of the model card.
            404:
                description: Either the card or at least one of the provided fields do not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        json_data = request.get_json()
        card = ModelCardEntry(ModelCard())
        if json_data:
            try: card.card.data.assign(dynamic2dict(json_data, {"title"}))
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
        """
        Autocompletes an already created model card given a string pointing to a repository URL or some file contents.
        This calls on an AI assistant to work on the card, blocking editing while the latter runs.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: assistant_type
            in: path
            type: string
            required: true
            description: The AI assistant type. Options available from get /assistants.
          - name: body
            description: A repository url starting with http:// or https://, or an uploaded readme text file's contents (can be the contents of a .txt, .md, or .html file).
            in: body
            required: true
            schema:
              type: string
        responses:
            200:
                description: Successfully submitted task.
            404:
                description: Resource does not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        json_data = request.get_json()
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        exists(isinstance(json_data, str), "Autocomplete requires a url string as POST data")
        status = exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.").autocomplete(json_data, assistant)
        return jsonify(status)

    @app.route('/assistant/<string:assistant_type>/refine/<int:card_id>', methods=['POST'])
    def autorefine_card(card_id: int, assistant_type: str):
        """
        Refines an already created model card so that its contents are easier to parse by laypeople.
        This calls on an AI assistant to work on the card, blocking editing while the latter runs.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: assistant_type
            in: path
            type: string
            required: true
            description: The AI assistant type. Options available from get /assistants.
        responses:
            200:
                description: Successfully submitted task.
            404:
                description: Resource does not exist.
            409:
                description: An AI assistant is working on the model card.
        """
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
