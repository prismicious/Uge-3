import os
from typing import List

from flask import json, jsonify
from models.Cereal import Cereal
from models.Filter import Filter
from dotenv import load_dotenv
import sqlite3

from utils import get_columns_and_placeholders, jsonify_result

load_dotenv()


class SQLiteClient():
    def __init__(self):
        self.table_name = "cereals"

    def connect(self):
        try:
            self.connection = sqlite3.connect("cereals.db")
            # This makes fetchall() return dictionaries
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

        except Exception as e:
            print(e)

    def create_table(self, table_name: str) -> str:
        # Directly define the columns and types for the schema
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            mfr VARCHAR(255),
            type_ VARCHAR(255),
            calories INT,
            protein FLOAT,
            fat FLOAT,
            sodium FLOAT,
            fiber FLOAT,
            carbo FLOAT,
            sugars FLOAT,
            potass FLOAT,
            vitamins FLOAT,
            shelf INT,
            weight FLOAT,
            cups FLOAT,
            rating FLOAT
        );
        """

        try:
            self.execute_query(query)
            return f"Table {table_name} created!"
        except Exception as e:
            print("Error creating table", e)

    def create(self, cereal: Cereal) -> str:
        query = f"INSERT INTO cereals (name, manufacturer, calories, protein, fat, sodium, fiber, carbo, sugars, potassium, vitamins, shelf, weight, cups, rating) VALUES {cereal}"
        try:
            self.cursor.execute(query)
            return "Cereal succesfully created!"
        except Exception as e:
            print("Error creating cereal", e)

    def read_all(self) -> List[Cereal]:
        query = "SELECT * FROM cereals"
        try:
            result = self.execute_query(query)

            return jsonify_result(result)

        except Exception as e:
            print("Error reading all cereals", e)

    def read(self, id: int) -> Cereal:
        query = f"SELECT * FROM cereals WHERE id = {id}"
        try:
            result = self.execute_query(query)
            return result
        except Exception as e:
            print("Error reading cereal", e)
            return None

    def update(self, id: int, data: Cereal) -> str:
        query = f"UPDATE cereals SET {data} WHERE id = {id}"
        try:
            self.cursor.execute(query)
            return f"Cereal updated!"
        except Exception as e:
            print("Error updating cereal", e)

    def delete(self, id: int) -> str:
        query = f"DELETE FROM cereals WHERE id = {id}"
        try:
            self.cursor.execute(query)
            return "Cereal deleted!"
        except Exception as e:
            print("Error deleting cereal", e)

    def list(self) -> List[Cereal]:
        query = "SELECT * FROM cereals"

        try:
            cereals = self.cursor.execute(query)
            return cereals

        except Exception as e:
            print("Error listing cereals", e)

    def filter(self, filters: List[Filter]):
        query = "SELECT * FROM cereals WHERE "
        conditions = []

        for filter in filters:
            condition = f"{filter.field} = {filter.value}"
            conditions.append(condition)

        # Join all the filter conditions with AND
        query += " AND ".join(conditions)

        try:
            result = self.execute_query(query)

            return jsonify_result(result)
        except Exception as e:
            print("Error filtering cereals", e)

    def does_product_exist(self, id: int) -> bool:
        result = self.read(id)

        if result:
            return True

        return False

    def insert_data(self, cereals: List[Cereal], table_name: str):
        self.create_table(table_name)

        columns, placeholders = get_columns_and_placeholders(cereals[0])

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Prepare the data to be inserted
        data = [
            (
                cereal.name, cereal.mfr, cereal.type_, cereal.calories, cereal.protein, cereal.fat,
                cereal.sodium, cereal.fiber, cereal.carbo, cereal.sugars, cereal.potass,
                cereal.vitamins, cereal.shelf, cereal.weight, cereal.cups, cereal.rating
            )
            for cereal in cereals  # This gathers all the cereal data
        ]

        result = self.execute_query(query, data)

        if result:
            return f"Data inserted successfully!"

    def execute_query(self, query, data=None):
        query_type = query.strip().split(" ")[0].upper()
        self.connect()
        try:
            if query_type == "SELECT":
                result = self.cursor.execute(query).fetchall()

            if query_type in ["INSERT", "UPDATE", "DELETE"]:
                if not data:
                    result = self.cursor.execute(query)
                else:
                    result = self.cursor.executemany(query, data)

            self.connection.commit()
            return result

        except Exception as e:
            print("Error inserting data: ", e)

        finally:
            self.connection.close()

    def drop_table(self, table_name: str) -> str:
        query = f"DROP TABLE IF EXISTS {table_name};"

        try:
            self.execute_query(query)
            return f"Table {table_name} dropped successfully!"
        except Exception as e:
            print(f"Error dropping table {table_name}: {e}")
            return f"Error dropping table {table_name}"
