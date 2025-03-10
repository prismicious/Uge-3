import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from models.SQLiteClient import SQLiteClient
from models.Cereal import Cereal
from utils import filter_query



class CerealAPI():
    def __init__(self, sql_client: SQLiteClient):
        self.app = Flask(__name__)
        self._register_routes()
        self.version_number = os.getenv("VERSION_NUMBER", "1.0")
        self.sql_client = sql_client

    def _register_routes(self):

        @self.app.route("/ping", methods=["GET"])
        def ping():
            return jsonify({"message": "Pong!"})

        @self.app.route("/cereals/add", methods=["POST"])
        def create_cereal():
            try:
                cereal = request.json
                self.sql_client.create("")

            except Exception as e:
                return jsonify({"error": str(e)}), 400

        @self.app.route("/cereals", methods=["GET"])
        def filter_cereals():
            # Check if there are any query parameters
            if not request.args:
                # If not, return all cereals
                return self.sql_client.read_all()
                
            
            query = filter_query(request.args)
            result = self.sql_client.filter(query)
            return result

        @self.app.route("/cereals/<int:id>", methods=["GET", "POST"])
        def handle_request(self, id):
            try:
                if request.method == "POST":
                        
                    data = request.json
                    cereal = Cereal.from_dict(data)
            
                if not id:
                    if request.json:
                        self.sql_client.create(cereal)
                        
                product_exists = self.sql_client.does_product_exist(id)
                
                if product_exists:
                    message = self.sql_client.update(id, cereal)
                    return jsonify({"message": message})
                
                else:
                    return jsonify({"error": "Cereal not found"}), 404
            
            except Exception as e:
                print("Error updating cereal", e)
                return jsonify({"error": str(e)}), 400

        @self.app.route("/cereals/<int:id>", methods=["DELETE"])
        def delete_cereal(id):
            try:
                result = self.sql_client.delete("", id)

                if result:
                    return jsonify({"message": "Cereal deleted"})

                else:
                    return jsonify({"error": "Cereal not found"}), 404

            except Exception as e:
                return jsonify({"error": str(e)}), 400

