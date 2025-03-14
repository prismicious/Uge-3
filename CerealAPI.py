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
            result, status_code = ApiResponse("success", "Pong!", 200)
            return result.to_json(), status_code

        @self.app.route("/cereals", methods=["GET", "POST"])
        def handle_cereals():
            if request.method == "GET":
                result, status_code = self.get_cereals()
                return result, status_code
            elif request.method == "POST":

                has_password = request.json.get('password')

                if not has_password:
                    return ApiResponse("error", "Password not set", 401).to_json(), 401

                authorised = is_authorised(request.json)

                if not authorised:
                    return ApiResponse("error", "Unauthorized", 401).to_json(), 401

                validation_error: ApiResponse = validate_request_body(request)

                if validation_error:
                    return validation_error.to_json(), 400

                result, status_code = self.create_or_update_cereal()
                return result, status_code

        @self.app.route("/cereals/<int:id>", methods=["GET", "POST", "DELETE"])
        def handle_cereal_by_id(id):
            try:
                if request.method == "GET":
                    result, status_code = self.get_cereal_by_id(id)
                    return result, status_code

                elif request.method == "POST":
                    validation_error = validate_request_body(request)
                    if validation_error:
                        return validation_error.to_json()
                    result, status_code = self.create_or_update_cereal()
                    return result, status_code

                elif request.method == "DELETE":
                    result, status_code = self.delete_cereal(id)
                    return result, status_code

            except Exception as e:
                return ApiResponse("error", str(e), 400).to_json(), 400

    def get_cereals(self):
        try:
            if not request.args:
                result = self.sql_client.read_all()
                return result.to_json(), result.status_code

            query = filter_query(request.args)
            result = self.sql_client.filter(query)
            return result.to_json(), result.status_code
        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400

    def create_or_update_cereal(self):
        try:
            data = request.json
            cereal = Cereal.from_dict(data)

            if not cereal.id:
                result = self.sql_client.create(cereal)
                return result.to_json(), result.status_code
            else:
                product_exists = self.sql_client.does_product_exist(cereal.id)

                if product_exists:
                    result = self.sql_client.update(cereal.id, cereal)
                    return result.to_json(), result.status_code
                else:
                    return ApiResponse("error", "Cereal not found", 404).to_json(), 404
        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400

    def get_cereal_by_id(self, id):
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
        try:
            result = self.sql_client.delete(id)

            return result.to_json(), result.status_code

        except Exception as e:
            return ApiResponse("error", str(e), 400).to_json(), 400
