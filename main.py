import threading
import time
from CerealAPI import CerealAPI
from models.Driver import Driver
from models.SQLiteClient import SQLiteClient
from models.parser import Parser


class Main:
    """
    This class is the entry point of the application
    It initializes the Parser, SQLiteClient, CerealAPI, and Driver classes
    """
    def __init__(self):
        self.parser = Parser() # Handles parsing of the CSV file
        self.cereals = self.parser.read_csv() # Turn .csv file into a list of Cereal objects
        self.sql_client = SQLiteClient() # Handles database operations
        self.cereal_api = CerealAPI(self.sql_client) # Handles API operations
        self.driver = Driver() # Tests the API

    def run(self):
        sql_client = self.sql_client
        
        # Insert the cereals into the database
        result = sql_client.insert_data(self.cereals)
        if result:
            print(result)
        
        def run_flask_app():
            self.cereal_api.app.run()
        
        # To ensure that the Flask app runs in a separate thread to avoid blocking the driver
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.start()
        
        print("Waiting for the Flask app to start...")
        time.sleep(3) # Wait for the Flask app to start (estimated time)
        self.driver.test_api()  

if __name__ == "__main__":
    app = Main()
    app.run()
