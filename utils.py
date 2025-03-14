import csv
import os
import dotenv
from flask import jsonify
from models.Filter import Filter
from models.ApiResponse import ApiResponse

dotenv.load_dotenv

password_from_env = os.getenv('PASSWORD', 'test_password')


def read_file(file):
    with open(file, 'r') as f:
        return f.read()


def filter_query(args):
    filters = []

    # Is there a better way to do this?

    filterable_fields = [
        'name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium',
        'fiber', 'carbo', 'sugars', 'potass', 'vitamins', 'shelf',
        'weight', 'cups', 'rating'
    ]

    for field in filterable_fields:
        if field not in args:
            continue

        value = args.get(field)

        filter = Filter(field, value)
        filters.append(filter)

    return filters


def get_columns_and_placeholders(cereal):
    dict_keys = cereal.__dict__.keys()
    # Exclude 'id' from the dictionary keys
    columns = ', '.join(key for key in dict_keys if key != 'id')
    placeholders = ', '.join(
        ['?'] * len([key for key in dict_keys if key != 'id']))

    return columns, placeholders


def get_assignments_and_values(cereal):
    dict_keys = cereal.__dict__.keys()
    assignments = ', '.join(f"{key} = ?" for key in dict_keys if key != 'id')
    values = tuple(
        value for key, value in cereal.__dict__.items() if key != 'id')

    return assignments, values


def jsonify_result(result):
    try:
        results = []

        for row in result:
            row_dict = dict(row)
            results.append(row_dict)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


def validate_request_body(request):
    if not request.is_json:
        return ApiResponse("error", "Request body must be JSON", 400)
    if not request.json:
        return ApiResponse("error", "Request body must not be empty", 400)
    return None  # If validation passes, return None


def is_successful(status_code):
    if status_code == 200:
        return True

    return False


def is_authorised(request_json):
    input_password = request_json.get('password')

    if input_password == password_from_env:
        return True

    return False
