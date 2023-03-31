# REST API Client and File Operations

This project demonstrates a Python script to interact with a REST API, manage user data, and perform file operations. It showcases how to use Python for creating a simple API client and file handler, which can be modified and extended for various software engineering projects.

## Features

- Send GET, POST, PUT, and DELETE requests to a REST API
- Manage user data (list, create, update, and delete users)
- Read and write data to a file

## Dependencies

- Python 3.6 or higher
- `requests` library

## Usage

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Replace the your_api_key placeholder in the main() function with your actual API key:
```python
rest_client = RESTClient("https://api.example.com", "your_api_key")
```

3. Run the script:
```bash
python main.py
```

The script will perform the following operations:
- Get a list of users and print them
- Create a new user and print the created user data
- Update an existing user and print the updated user data
- Delete a user and print the user ID of the deleted user
- Write data to a file named output.txt
- Read data from the file and print the contents

## Customization
You can modify the main() function to perform different operations with the UserManager and OutputFile classes. You can also extend the classes to add more functionality as needed for your specific project.

## License
This project is released under the [MIT License.](https://opensource.org/license/mit/)