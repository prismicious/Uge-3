import os
from flask import jsonify
from typing import List
from models.ApiResponse import ApiResponse
from models.Cereal import Cereal
from models.Filter import Filter
from dotenv import load_dotenv
import sqlite3
from utils import get_assignments_and_values, get_columns_and_placeholders, is_successful

load_dotenv()


class SQLiteClient:
    """
    This class is responsible for handling all database operations.
    It initializes the database and provides methods for CRUD operations on the 'cereals' table.
    It also provides methods for filtering and listing cereals.
    It uses the method execute_query to execute SQL queries on the database.
        - execute_query returns an ApiResponse object with the appropriate response and status code.
    Execute_db_operation is a wrapper around execute_query that ensures the appropriate success message is returned.
    Every method returns an ApiResponse object.
    """
    def __init__(self):
        self.table_name = "cereals"
        self._initialize_db()

    def connect(self):
        connection = sqlite3.connect("cereals.db")
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_db(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
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
        result = self.execute_query(query)

        if result:
            print("Database initialized successfully")

    def create(self, cereal: Cereal) -> ApiResponse:        
        data = [
            cereal.name, cereal.mfr, cereal.type_, cereal.calories, cereal.protein, cereal.fat,
            cereal.sodium, cereal.fiber, cereal.carbo, cereal.sugars, cereal.potass,
            cereal.vitamins, cereal.shelf, cereal.weight, cereal.cups, cereal.rating
        ]
        columns, placeholders = get_columns_and_placeholders(cereal)
        query = f"INSERT INTO cereals ({columns}) VALUES ({placeholders})"
        result = self.execute_db_operation(
            query, data, "Created cereal successfully")

        return result

    def read_all(self) -> ApiResponse:
        query = "SELECT * FROM cereals"
        result = self.execute_db_operation(
            query, None, "Fetched all cereals successfully")
        return result

    def read(self, id: int) -> ApiResponse:
        query = "SELECT * FROM cereals WHERE id = ?"
        result = self.execute_db_operation(
            query, (id,), "Fetched cereal successfully")
        return result

    def update(self, id: int, cereal: Cereal) -> ApiResponse:
        assignments, values = get_assignments_and_values(cereal)
        query = f"UPDATE cereals SET {assignments} WHERE id = ?"
        data = values + (id,)
        result = self.execute_db_operation(
            query, data, "Updated cereal successfully")
        return result

    def delete(self, id: int) -> ApiResponse:
        cereal = self.read(id).data
        
        if not cereal:
            return ApiResponse("error", "Cereal not found", 404)
        
        query = "DELETE FROM cereals WHERE id = ?"
        data = (id,)
        result = self.execute_db_operation(
            query, data, "Deleted cereal successfully")

        return result

    def list(self) -> ApiResponse:
        query = "SELECT * FROM cereals"
        result = self.execute_db_operation(
            query, None, "Fetched all cereals successfully")

        return result

    def filter(self, filters: List[Filter]) -> ApiResponse:
        conditions = " AND ".join(f"{f.field} = ?" for f in filters)
        values = [f.value for f in filters]
        query = f"SELECT * FROM cereals WHERE {conditions}"
        result = self.execute_db_operation(query, tuple(
            values), f"Filtered cereals successfully")

        if result.data:
            result.message = f"Found {len(result.data)} cereals for filters"
            return result

        else:
            return ApiResponse("error", f"No cereals found for filters", 404)

    def does_product_exist(self, id: int) -> bool:
        result = self.read(id)
        return bool(result.data)

    def insert_data(self, cereals: List[Cereal]) -> ApiResponse:
        columns, placeholders = get_columns_and_placeholders(cereals[0])
        # Make sure to use INSERT OR IGNORE to avoid inserting duplicate data
        query = f"INSERT OR IGNORE INTO cereals ({columns}) VALUES ({placeholders})"
        data = [(
            cereal.name, cereal.mfr, cereal.type_, cereal.calories, cereal.protein, cereal.fat,
            cereal.sodium, cereal.fiber, cereal.carbo, cereal.sugars, cereal.potass,
            cereal.vitamins, cereal.shelf, cereal.weight, cereal.cups, cereal.rating
        ) for cereal in cereals]
        result = self.execute_db_operation(
            query, data, "Inserted cereals successfully", multiple=True)
        return result

    def execute_query(self, query: str, data=None, multiple=False) -> ApiResponse:
        """
        This method is used to execute SQL queries on the database.
        It returns an ApiResponse object with the appropriate response and status code.
        """
        query_type = query.strip().split(" ")[0].upper()

        try:
            with self.connect() as connection:
                cursor = connection.cursor()

                # This handles CREATE queries. It currently only supports CREATE TABLE queries.

                if query_type == "CREATE":
                    result = cursor.execute(query)
                    return result

                if query_type == "SELECT":
                    cursor.execute(query, data or [])
                    result = cursor.fetchall()
                    data = [dict(row) for row in result]
                    return ApiResponse("success", "Query executed successfully", 200, data)

                """
                The following block of code is used to handle INSERT, UPDATE, and DELETE queries.
                It returns a different response and status code based on the query type.
                INSERT: 201 (Created)
                UPDATE: 200 (OK)
                DELETE: 204 (No Content/Deleted)
                """
                if query_type == "INSERT":
                    if multiple:
                        cursor.executemany(query, data)
                    else:
                        cursor.execute(query, data)
                        connection.commit()
                    return ApiResponse("success", "Resource created successfully", 201)

                if query_type == "UPDATE":
                    cursor.execute(query, data)
                    connection.commit()
                    return ApiResponse("success", "Resource updated successfully", 201)

                if query_type == "DELETE":
                    cursor.execute(query, data)
                    connection.commit()
                    return ApiResponse("success", "Resource deleted successfully", 200)

        except sqlite3.Error as e:
            return ApiResponse("error", "Database query failed", 500, details=str(e))

    def execute_db_operation(self, query: str, params: tuple, success_message: str, multiple=None) -> ApiResponse:
        """
        This method functions as a wrapper around the execute_query method.
        It ensures that the appropriate success message is returned based on the query type.   
        """
        result = self.execute_query(query, params, multiple)
        if is_successful(result.status_code):
            result.set_message(success_message)

        return result

    # This method is used to drop the table if it exists. It is useful for testing purposes.
    def drop_table(self) -> ApiResponse:
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        return self.execute_query(query)
