import os
from flask import Flask, request


from models.SQLiteClient import SQLiteClient
from models.Cereal import Cereal
from utils import filter_query, is_authorised, validate_request_body
from models.ApiResponse import ApiResponse


class CerealAPI():
    """
    This class is responsible for handling all API operations.
    It initializes the Flask app and registers the routes for the API.
    The routes are:
    - /ping: Returns "Pong!" if the API is running
    - /cereals: GET - Returns all cereals, POST - Creates a new cereal
    - /cereals/<id>: GET - Returns a cereal by ID, POST - Updates a cereal by ID, DELETE - Deletes a cereal by ID
    The response always returns a jsonified ApiResponse object.
    """
    def __init__(self, sql_client: SQLiteClient):
        self.app = Flask(__name__)
        self._register_routes()
        self.app.url_map.strict_slashes = False  # Disable strict slashes
        self.sql_client = sql_client
        self.app.config['JSON_SORT_KEYS'] = False  # Disable sorting of keys

    def _register_routes(self):
        @self.app.route("/ping", methods=["GET"])
        def ping():
            result, status_code = ApiResponse("success", "Pong!", 200)
            return result.to_json(), status_code

        @self.app.route("/cereals", methods=["GET", "POST"])
        def handle_cereals():
        # This function handles GET and POST requests to the /cereals endpoint
            if request.method == "GET":
                result, status_code = self.get_cereals()
                return result, status_code
            elif request.method == "POST":
                try:
                    request.json.get('password')
                    
                except Exception as e:
                    return ApiResponse("error", str(e), 400).to_json(), 400

                authorised = is_authorised(request.json)

                if not authorised:
                    return ApiResponse("error", "Unauthorized", 401).to_json(), 401

                validation_error: ApiResponse = validate_request_body(request)

                if validation_error:
                    return validation_error.to_json(), 400
                
                id = request.json.get('id')

                result, status_code = self.create_or_update_cereal(id)
                return result, status_code

        @self.app.route("/cereals/<int:id>", methods=["GET", "POST", "DELETE"])
        def handle_cereal_by_id(id):
        # This function handles GET, POST, and DELETE requests to the /cereals/<id> endpoint
            try:
                if request.method == "GET":
                    result, status_code = self.get_cereal_by_id(id)
                    return result, status_code

                elif request.method == "POST":
                    try:
                        request.json.get('password')
                        
                    except Exception as e:
                        return ApiResponse("error", str(e), 400).to_json(), 400
                    
                    authorised = is_authorised(request.json)

                    if not authorised:
                        return ApiResponse("error", "Unauthorized", 401).to_json(), 401

                    # We need to check if the request body is JSON or if it exists
                    validation_error = validate_request_body(request)
                    if validation_error:
                        return validation_error.to_json()
                    result, status_code = self.create_or_update_cereal(id)
                    return result, status_code

                elif request.method == "DELETE":
                    try:
                        request.json.get('password')
                        
                    except Exception as e:
                        return ApiResponse("error", str(e), 400).to_json(), 400

                    authorised = is_authorised(request.json)

                    if not authorised:
                        return ApiResponse("error", "Unauthorized", 401).to_json(), 401

                    result, status_code = self.delete_cereal(id)  
                    
                    return result, status_code

            except Exception as e:
                return ApiResponse("error", str(e), 400).to_json(), 400

    def get_cereals(self):
        """
        Handles the business logic for getting all cereals or filtering cereals based on query parameters.
        """
        try:
            if not request.args:
                result = self.sql_client.read_all()
                return result.to_json(), result.status_code

            query = filter_query(request.args)
            result = self.sql_client.filter(query)
            return result.to_json(), result.status_code
        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400

    def create_or_update_cereal(self, id):
        """
        Handles the business logic for creating or updating a cereal.
        """
        try:
            data = request.json
            cereal = Cereal.from_dict(data)

            if not id:
                result = self.sql_client.create(cereal)
                return result.to_json(), result.status_code
            else:
                product_exists = self.sql_client.does_product_exist(id)

                if product_exists:
                    result = self.sql_client.update(cereal.id, cereal)
                    return result.to_json(), result.status_code
                else:
                    return ApiResponse("error", "Cereal not found", 404).to_json(), 404
        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400

    def get_cereal_by_id(self, id):
        """
        Handles the business logic for getting a cereal by ID.
        """
        try:
            product_exists = self.sql_client.does_product_exist(id)

            if product_exists:
                result = self.sql_client.read(id)
                return result.to_json(), result.status_code
            else:
                return ApiResponse("error", "Cereal not found", 404).to_json(), 404

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400

    def update_cereal(self, id, data):
        """Handles the business logic for updating a cereal."""
        try:
            cereal = Cereal.from_dict(data)

            product_exists = self.sql_client.does_product_exist(id)

            if product_exists:
                result = self.sql_client.update(id, cereal)
                return result.to_json(), result.status_code
            else:
                return ApiResponse("error", "Cereal not found", 404).to_json(), 404

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400

    def delete_cereal(self, id):
        """Handles the business logic for deleting a cereal."""
        try:
            result = self.sql_client.delete(id)

            return result.to_json(), result.status_code

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400
