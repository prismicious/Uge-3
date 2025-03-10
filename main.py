from CerealAPI import CerealAPI
from models.SQLiteClient import SQLiteClient
from models.parser import Parser


class Main:
    def __init__(self):
        self.parser = Parser()
        self.cereals = self.parser.read_csv()
        self.sql_client = SQLiteClient()
        self.cereal_api = CerealAPI(self.sql_client)
        
    def run(self):
        sql_client = self.sql_client
        result = sql_client.insert_data(self.cereals, "cereals")
        if result:
            print(result)
            
        self.cereal_api.app.run()
    
if __name__ == "__main__":
    app = Main()
    app.run()