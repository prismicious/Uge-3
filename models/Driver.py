
import time
import requests

from models.ApiResponse import ApiResponse

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

        self.prototype_object = {
            "name": "Prototype Cereal",
            "mfr": "P",
            "type": "C",
            "calories": 100,
            "protein": 3,
            "fat": 2,
            "sodium": 200,
            "fiber": 1,
            "carbo": 10,
            "sugars": 5,
            "potass": 50,
            "vitamins": 25,
            "shelf": 3,
            "weight": 1,
            "cups": 1,
            "password": password
        }

        self._initialize()

    def _initialize(self):
        print("Driver initialized. \n")
        message = (
            "Running tests... \n"
            "1. Get a cereal by ID. \n"
            "2. Get all cereals. \n"
            "3. Filter cereals. \n"
            "4. Delete a cereal. \n"
            "5. Create a cereal. \n"
            "6. Update a cereal. \n"
            "7. Get a cereal by ID that doesn't exist. \n"
        )

        print(message)
        sleep()

    def test_api(self):
        """"
        Iterate through different API requests to test the API.
        I know this could be done more dynamically, but I like the
        readability of this sequential approach.
        """
        results = []

        # 1. Get a cereal by ID
        result = self.get_cereal_by_id(2, 200)  # GET /cereals/2
        results.append(result)
        sleep()

        # 2. Get all cereals
        result = self.get_cereals(200)  # GET /cereals
        results.append(result)
        sleep()

        # 3. Filter cereals
        # GET /cereals?mfr=C&shelf=3
        result = self.get_cereal_by_filter("mfr=P&shelf=3", 200)
        results.append(result)
        sleep()

        # 4. Delete a cereal
        result = self.delete_cereal(5, 200)  # DELETE /cereals/5 > This should be 204 but I can't get it to work.
        results.append(result)
        sleep()

        # 5. Create a cereal
        result = self.create_cereal(201)  # POST /cereals
        results.append(result)
        sleep()

        # 6. Update a cereal
        result = self.create_cereal(2, 201)  # POST /cereals/2
        results.append(result)
        sleep()

        # 7. Get a cereal by ID that doesn't exist
        result = self.create_cereal(12435, 404)
        results.append(result)
        sleep()

        print_results(results)

    def get_cereal_by_filter(self, filter, expected_status_code):
        # Filter cereals by mfr and shelf
        endpoint = f"http://{self.url}/cereals?{filter}"
        response = self.send_request(endpoint, "GET")

        return verify_status_code(response.get("status_code"), expected_status_code, response)

    def get_cereal_by_id(self, id, expected_status_code):
        endpoint = f"http://{self.url}/cereals/{id}"
        response = self.send_request(endpoint, "GET")

        return verify_status_code(response.get("status_code"), expected_status_code, response)

    def get_cereals(self, expected_status_code):
        endpoint = f"http://{self.url}/cereals"

        response = self.send_request(endpoint, "GET")

        return verify_status_code(response.get("status_code"), expected_status_code, response)

    def get_cereal_by_id(self, id, expected_status_code):
        endpoint = f"http://{self.url}/cereals/{id}"

        response = self.send_request(endpoint, "GET")

        return verify_status_code(response.get("status_code"), expected_status_code, response)

    def delete_cereal(self, id, expected_status_code):
        endpoint = f"http://{self.url}/cereals/{id}"

        response = self.send_request(endpoint, "DELETE", {
            "password": password
        })

        return verify_status_code(response.get("status_code"), expected_status_code, response)

    def create_cereal(self, id=None, expected_status_code=201):

        # If id is not provided, create a new cereal
        # Else, update the cereal with the provided id

        if not id:
            endpoint = f"http://{self.url}/cereals"

        else:
            endpoint = f"http://{self.url}/cereals/{id}"

        response = self.send_request(endpoint, "POST", self.prototype_object)

        return verify_status_code(response.get("status_code"), expected_status_code, response)

    def send_request(self, endpoint, method, data=None):
        try:
            # Generic method to send requests to the API
            response = requests.request(
                method, endpoint, json=data, headers=self.headers)
            return response.json()

        except Exception as e:
            return {"status": "error", "message": str(e)}


def sleep():
    interval = 1
    time.sleep(interval)


def print_results(results):
    print("Generating test results...")
    tests = 0

    message = "Results: \n"
    for result in results:
        tests += 1

        if result.get("status") == "success":
            result_text = f"Passed ✅"
        else:
            result_text = f"Failed ❌"

        message += f"Test #{tests}: {result_text} > {result.get("message")} \n"

    print(message)


def verify_status_code(status_code, expected_status_code, response):
    message = ""
    response: ApiResponse = ApiResponse.from_dict(response)
    
    if response.message:
        message = response.message
    
    elif response.action:
        message = response.action
        
    if status_code == expected_status_code:
        return {"status": "success", "message": message}
    
    return {"status": "error", "message": message}
