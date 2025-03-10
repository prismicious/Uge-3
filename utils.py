import csv

from flask import jsonify
from models.Filter import Filter


def read_file(file):
    with open(file, 'r') as f:
        return f.read()
    
def filter_query(args):    
    filters = []
    
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
    columns = ', '.join(cereal.__dict__.keys())
    placeholders = ', '.join(['?'] * len(cereal.__dict__))
    
    return columns, placeholders
    
def jsonify_result(result):
    try:
        results = []
        
        for row in result:
            row_dict = dict(row)
            results.append(row_dict)
            
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400