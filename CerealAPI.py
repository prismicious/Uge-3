import os
from flask import Flask, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
    
from models.SQLiteClient import SQLiteClient
from models.Cereal import Cereal
from utils import filter_query, is_authorised, validate_request_body
from models.ApiResponse import ApiResponse


class CerealAPI():
    def __init__(self, sql_client: SQLiteClient):
        self.app = Flask(__name__)
        self._register_routes()
        self.app.url_map.strict_slashes = False  # Disable strict slashes
        self.sql_client = sql_client
        self._register_swagger()
        self.app.config['JSON_SORT_KEYS'] = False  # Disable sorting of keys

    def _register_swagger(self):
        SWAGGER_URL = "/cereals/swagger"
        API_URL = "/swagger.json"

        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL, API_URL, config={"app_name": "Cereal API"}
        )
        
        self.app.register_blueprint(
            swaggerui_blueprint, url_prefix=SWAGGER_URL)

        @self.app.route("/swagger.json")
        def swagger_json():
            return send_from_directory("static", "swagger.json")

    def _register_routes(self):
        @self.app.route("/ping", methods=["GET"])
        def ping():
            result = ApiResponse("success", "Pong!", 200)
            return result.to_json()

        @self.app.route("/cereals", methods=["GET", "POST"])
        def handle_cereals():
            if request.method == "GET":
                return self.get_cereals()
            elif request.method == "POST":
                
                has_password = request.json.get('password')
                
                if not has_password:
                    return ApiResponse("error", "Password not set", 401).to_json()
                
                authorised = is_authorised(request.json)
                
                if not authorised:
                    return ApiResponse("error", "Unauthorized", 401).to_json()
                
                validation_error: ApiResponse = validate_request_body(request)

                if validation_error:
                    return validation_error.to_json()

                return self.create_or_update_cereal()

        @self.app.route("/cereals/<int:id>", methods=["GET", "POST", "DELETE"])
        def handle_cereal_by_id(id):
            try:
                if request.method == "GET":
                    return self.get_cereal_by_id(id)

                elif request.method == "POST":
                    validation_error = validate_request_body(request)
                    if validation_error:
                        return validation_error.to_json()
                    return self.update_cereal(id, request.json)

                elif request.method == "DELETE":
                    return self.delete_cereal(id)

            except Exception as e:
                return ApiResponse("error", str(e), 400).to_json()

    def get_cereals(self):
        try:
            if not request.args:
                result = self.sql_client.read_all()
                return result.to_json()

            query = filter_query(request.args)
            result = self.sql_client.filter(query)
            return result.to_json()
        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json()

    def create_or_update_cereal(self):
        try:
            data = request.json
            cereal = Cereal.from_dict(data)

            if not cereal.id:
                result = self.sql_client.create(cereal)
                return result.to_json()
            else:
                product_exists = self.sql_client.does_product_exist(cereal.id)

                if product_exists:
                    return self.sql_client.update(cereal.id, cereal).to_json()
                else:
                    return ApiResponse("error", "Cereal not found", 404).to_json()
        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json()

    def get_cereal_by_id(self, id):
        try:
            product_exists = self.sql_client.does_product_exist(id)

            if product_exists:
                return self.sql_client.read(id).to_json()
            else:
                return ApiResponse("error", "Cereal not found", 404).to_json()

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json()

    def update_cereal(self, id, data):
        try:
            cereal = Cereal.from_dict(data)

            product_exists = self.sql_client.does_product_exist(id)

            if product_exists:
                return self.sql_client.update(id, cereal).to_json()
            else:
                return ApiResponse("error", "Cereal not found", 404).to_json()

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json()

    def delete_cereal(self, id):
        try:
            result = self.sql_client.delete(id)

            return result.to_json()

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json()
