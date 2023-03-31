# Import required libraries
import os
import sys
import time
from datetime import datetime
import json
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode

# Define custom exception for API errors
class APIError(Exception):
    pass

# Define custom exception for file handling errors
class FileHandlingError(Exception):
    pass

# Define a class to interact with the REST API
class RESTClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _build_url(self, endpoint, params=None):
        """
        Build a URL for the REST API request.

        :param endpoint: API endpoint
        :type endpoint: str
        :param params: Query parameters (optional)
        :type params: dict
        :return: Full URL
        :rtype: str
        """
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        query_string = urlencode(params)
        return f"{self.base_url}/{endpoint}?{query_string}"

    def _send_request(self, method, endpoint, params=None, data=None):
        """
        Send an HTTP request to the REST API.

        :param method: HTTP method (GET, POST, PUT, DELETE)
        :type method: str
        :param endpoint: API endpoint
        :type endpoint: str
        :param params: Query parameters (optional)
        :type params: dict
        :param data: Request payload (optional)
        :type data: dict
        :return: Response data
        :rtype: dict
        :raises APIError: If the API request failed
        """
        url = self._build_url(endpoint, params)
        try:
            response = requests.request(method, url, json=data)
            response.raise_for_status()
        except RequestException as e:
            raise APIError(f"API request failed: {e}")

        try:
            return response.json()
        except ValueError:
            return None

    def get(self, endpoint, params=None):
        """
        Send a GET request to the REST API.

        :param endpoint: API endpoint
        :type endpoint: str
        :param params: Query parameters (optional)
        :type params: dict
        :return: Response data
        :rtype: dict
        """
        return self._send_request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        """
        Send a POST request to the REST API.

        :param endpoint: API endpoint
        :type endpoint: str
        :param data: Request payload (optional)
        :type data: dict
        :return: Response data
        :rtype: dict
        """
        return self._send_request("POST", endpoint, data=data)

    def put(self, endpoint, data=None):
        """
        Send a PUT request to the REST API.

        :param endpoint: API endpoint
        :type endpoint: str
        :param data: Request payload (optional)
        :type data: dict
        :return: Response data
        :rtype: dict
        """
        return self._send_request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        """
        Send a DELETE request to the REST API.

        :param endpoint: API endpoint
        :type endpoint: str
        :return: Response data
        :rtype: dict
        """
        return self._send_request("DELETE", endpoint)

# Define a class to manage user data
class UserManager:
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def get_users(self, page=1, per_page=10):
        """
        Get a list of users.

        :param page: Page number (optional)
        :type page: int
        :param per_page: Number of items per page (optional)
        :type per_page: int
        :return: List of users
        :rtype: list
        """
        params = {"page": page, "per_page": per_page}
        return self.rest_client.get("users", params=params)

    def get_user(self, user_id):
        """
        Get a single user.

        :param user_id: User ID
        :type user_id: int
        :return: User data
        :rtype: dict
        """
        return self.rest_client.get(f"users/{user_id}")

    def create_user(self, user_data):
        """
        Create a new user.

        :param user_data: User data
        :type user_data: dict
        :return: Created user data
        :rtype: dict
        """
        return self.rest_client.post("users", data=user_data)

    def update_user(self, user_id, user_data):
        """
        Update a user.

        :param user_id: User ID
        :type user_id: int
        :param user_data: User data
        :type user_data: dict
        :return: Updated user data
        :rtype: dict
        """
        return self.rest_client.put(f"users/{user_id}", data=user_data)

    def delete_user(self, user_id):
        """
        Delete a user.

        :param user_id: User ID
        :type user_id: int
        :return: Response data
        :rtype: dict
        """
        return self.rest_client.delete(f"users/{user_id}")

# Define a class to manage the output file
class OutputFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_data(self, data):
        """
        Write data to the output file.

        :param data: Data to write
        :type data: str
        :raises FileHandlingError: If the file could not be written
        """
        try:
            with open(self.file_path, "w") as file:
                file.write(data)
        except IOError as e:
            raise FileHandlingError(f"Could not write to file: {e}")

    def read_data(self):
        """
        Read data from the output file.

        :return: File contents
        :rtype: str
        :raises FileHandlingError: If the file could not be read
        """
        try:
            with open(self.file_path, "r") as file:
                return file.read()
        except IOError as e:
            raise FileHandlingError(f"Could not read from file: {e}")

def main():
    # Initialize REST client and user manager
    rest_client = RESTClient("https://api.example.com", "your_api_key")
    user_manager = UserManager(rest_client)

    # Get a list of users
    users = user_manager.get_users(page=1, per_page=10)
    print("List of users:")
    for user in users:
        print(f"{user['id']} - {user['name']}")

    # Create a new user
    new_user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
    }
    new_user = user_manager.create_user(new_user_data)
    print(f"Created user: {new_user['id']} - {new_user['name']}")

    # Update an existing user
    user_id_to_update = 1
    updated_user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "555-987-6543",
    }
    updated_user = user_manager.update_user(user_id_to_update, updated_user_data)
    print(f"Updated user: {updated_user['id']} - {updated_user['name']}")

    # Delete a user
    user_id_to_delete = 2
    user_manager.delete_user(user_id_to_delete)
    print(f"Deleted user: {user_id_to_delete}")

    # Initialize the output file
    output_file = OutputFile("output.txt")

    # Write data to the output file
    data_to_write = "This is an example of writing data to a file."
    output_file.write_data(data_to_write)
    print(f"Data written to the file: {data_to_write}")

    # Read data from the output file
    file_contents = output_file.read_data()
    print(f"Data read from the file: {file_contents}")

if __name__ == "__main__":
    main()
