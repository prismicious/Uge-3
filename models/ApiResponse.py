from flask import jsonify


class ApiResponse:
    def __init__(self, status: str, action: str, status_code: int, data=None, details=None, message=None):
        self.status = status  # "success" or "error"
        self.action = action  # A message to the user
        self.status_code = status_code  # Always include the status code
        self.data = data  # If the response includes data, it goes here
        self.details = details  # Optional field for debugging
        self.message = message  # Optional field for the action that was performed

    def to_dict(self):
        response = {
            "status": self.status,
            "message": self.message,
            "action": self.action,
            "status_code": self.status_code,
            "data": self.data,  # None will be skipped if it's not provided
            "details": self.details  # Same for details
        }
        
        # Remove None values from the response dictionary
        return {k: v for k, v in response.items() if v is not None}

    def set_message(self, message):
        # Useful for setting a message after the ApiResponse object has been created
        self.message = message

    def to_json(self):
        return jsonify(self.to_dict())

    def __str__(self):
        return f"ApiResponse(status={self.status}, action={self.action}, status_code={self.status_code}, details={self.details}, message={self.message})"