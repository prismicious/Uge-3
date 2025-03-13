
import time
import requests

# Password for the API, also stored in .env,
# But this is just for testing purposes
password = "test_password"


class Driver():
    """
    This class is used to test the API
    I don't know if it's reasonable,
    instead of using a testing framework like pytest?
    """

    def __init__(self):
        # Set the URL and headers for the API requests
        self.url = "127.0.0.1:5000"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def test_api(self):
        """"Iterate through different API requests to test the API"""

        # 1. Get a cereal by ID
        self.get_cereal_by_id(2)  # GET /cereals/2
        sleep()

        # 2. Get all cereals
        self.get_cereals()  # GET /cereals
        sleep()

        # 3. Filter cereals
        # GET /cereals?mfr=C&shelf=3
        self.get_cereal_by_filter("mfr=C&shelf=3")
        sleep()

        # 4. Delete a cereal
        self.delete_cereal(5)  # DELETE /cereals/5
        sleep()

        # 5. Create a cereal
        self.create_cereal()  # POST /cereals
        sleep()

        # 6. Update a cereal
        self.create_cereal(2)  # POST /cereals/2
        sleep()

        # 7. Get a cereal by ID that doesn't exist
        self.create_cereal(12435)
        sleep()

    def get_cereal_by_filter(self, filter):
        # Filter cereals by mfr and shelf
        endpoint = f"http://{self.url}/cereals?{filter}"
        result = self.send_request(endpoint, "GET")
        print_result(result)

    def get_cereal_by_id(self, id):
        endpoint = f"http://{self.url}/cereals/{id}"
        result = self.send_request(endpoint, "GET")

        print_result(result)

    def get_cereals(self):
        endpoint = f"http://{self.url}/cereals"

        result = self.send_request(endpoint, "GET")

        print_result(result)

    def get_cereal_by_id(self, id):
        endpoint = f"http://{self.url}/cereals/{id}"

        result = self.send_request(endpoint, "GET")

        print_result(result)

    def delete_cereal(self, id):
        endpoint = f"http://{self.url}/cereals/{id}"

        result = self.send_request(endpoint, "DELETE")

        print_result(result)

    def create_cereal(self, id=None):

        # If id is not provided, create a new cereal
        # Else, update the cereal with the provided id

        if not id:
            endpoint = f"http://{self.url}/cereals"

        else:
            endpoint = f"http://{self.url}/cereals/{id}"

        result = self.send_request(endpoint, "POST", {
            "name": "Cocoa Puffs",
            "manufacturer": "General Mills",
            "calories": 110,
            "protein": 1,
            "fat": 1,
            "sodium": 180,
            "fiber": 0,
            "carbo": 12,
            "sugars": 13,
            "potass": 55,
            "vitamins": 25,
            "shelf": 2,
            "weight": 1,
            "cups": 1,
            "password": password
        })

        print_result(result)

    def send_request(self, endpoint, method, data=None):
        # Generic method to send requests to the API
        response = requests.request(
            method, endpoint, json=data, headers=self.headers)
        return response.json()


def sleep():
    interval = 2
    time.sleep(interval)

def print_result(result):
    if result.get("message"):
        print(result.get("message"))
        return

    if result.get("status") == "error":
        print(f"Error: {result.get('action')}")
        return
    
    else:
        print(result.get("status_code"))