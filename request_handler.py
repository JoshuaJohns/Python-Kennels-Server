import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (
    get_all_animals,
    get_single_animal,
    get_all_locations,
    get_single_location,
    get_all_employees,
    get_single_employee,
    get_all_customers,
    get_single_customer,
    create_animal,
    create_location,
    create_customer,
    create_employee,
    delete_animal,
    delete_employee,
    delete_location,
    delete_customer,
    update_employee,
    update_customer,
    update_animal,
    update_location,
    get_customers_by_email,
    get_animals_by_location,
    get_animals_by_status,
    get_employees_by_location,
)


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        parsed = self.parse_url(self.path)

        if "?" not in self.path:
            (resource, id, query_params) = parsed
            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals(query_params)
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()
            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()
        else:  # There is a ? in the path, run the query param functions
            (resource, id, query) = parsed

            # see if the query dictionary has an email key
            if resource == "customers":
                response = get_customers_by_email(query[0])

            if resource == "animals":
                response = get_all_animals(query)
        # if query.get("status") and resource == "animals":
        #   response = get_animals_by_status(query["status"][0])

        # if query.get("location_id") and resource == "employees":
        #     response = get_employees_by_location(query["location_id"][0])
        # Parse the URL and capture the tuple that is returned

        # Send a JSON formatted string as a response
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server"""

        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        # response = {"payload": post_body}
        # Convert JSON string into Python dictionary
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        if resource == "animals":
            new_animal = create_animal(post_body)
        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_animal).encode())

        # New Location
        new_location = None
        if resource == "locations":
            new_location = create_location(post_body)
        self.wfile.write(json.dumps(new_location).encode())

        # New Employee
        new_employee = None
        if resource == "employees":
            new_employee = create_employee(post_body)
        self.wfile.write(json.dumps(new_employee).encode())

        # New Customer
        new_customer = None
        if resource == "customers":
            new_customer = create_customer(post_body)
        self.wfile.write(json.dumps(new_customer).encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

        if resource == "employees":
            delete_employee(id)

        self.wfile.write("".encode())

        if resource == "locations":
            delete_location(id)
        self.wfile.write("".encode())

        if resource == "customers":
            delete_customer(id)
        self.wfile.write("".encode())

    # A method that handles a PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

        if resource == "employees":
            update_employee(id, post_body)

        self.wfile.write("".encode())

        if resource == "locations":
            update_location(id, post_body)

        self.wfile.write("".encode())

        if resource == "customers":
            update_customer(id, post_body)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

        # def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        # path_params = path.split("/")
        # resource = path_params[1]
        # id = None

        # Try to get the item at index 2
        # try:
        # Convert the string "1" to the integer 1
        # This is the new parseInt()
        #    id = int(path_params[2])
        # except IndexError:
        #   pass  # No route parameter exists: /animals
        # except ValueError:
        #    pass  # Request had trailing slash: /animals/

        # return (resource, id)  # This is a tuple

        # def parse_url(self, path):
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != "":
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
