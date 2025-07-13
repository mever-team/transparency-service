from modelcard.card import ModelCard
from modelcard.service.assistant import Assistant
from flask import Flask, jsonify, request, abort, redirect
from flasgger import Swagger
from threading import Lock, Thread


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
        print("really ended completion", self.__is_completing)

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
        self.__thread = Thread(target=self.__autocomplete, args=(assistant,))
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
            "version": "0.0.1"
        }
    })
    test_data: dict[int, ModelCardEntry | None] = dict()

    @app.route("/", methods=['GET'])
    def get_index():
        return redirect(redirect_index, code=307)

    @app.route('/cards', methods=['GET'])
    def get_cards():
        """
        Retrieves a list of model cards.
        ---
        responses:
            200:
                description: A list of integer identifiers.
                schema:
                    type: array
                    items:
                        type: integer
        """
        return jsonify([key for key, value in test_data.items() if value is not None])

    @app.route('/assistants', methods=['GET'])
    def get_assistants():
        """
        Retrieves all available AI assistants for the current user and card and their descriptions.
        ---
        responses:
            200:
                description: A dictionary mapping assistant names to their descriptions.
                schema:
                  type: object
                  additionalProperties:
                    type: string
                    description: The description of the assistant.
        """
        return jsonify({key: value.description for key, value in assistants.items()})

    @app.route('/card/<int:card_id>', methods=['GET'])
    def get_card(card_id):
        """
        Retrieves the JSON data for a given model card.
        ---
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
                  description: The model card contents.
            404:
                description: The requested card does not exist or has been deleted.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(test_data.get(card_id, None), "Model card does not exist or has been deleted.") as card:
            return jsonify(card.data)

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
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: body
            in: body
            required: true
            description: Partial or full model card JSON to update the card with.
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
            try: card.data.assign(json_data)
            except AssertionError as e: abort(404, "Wrong data: "+str(e))
            except Exception as e: abort(404, "Wrong data: "+str(e))
            return jsonify(card.data)

    @app.route('/card', methods=['POST'])
    def create_card():
        """
        Creates a model card given an optional json representation - the representation is for manual upload.
        The provided json data should be either an empty dict or (parts of) a model card's
        json representation with potentially some missing fields, and updates everything in the
        target card. The card's contents after setting everything are retrieved.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
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
            try: card.card.data.assign(json_data)
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
