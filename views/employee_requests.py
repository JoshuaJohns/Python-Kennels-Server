import sqlite3
import json
from models.employee import Employee
from models.location import Location

EMPLOYEES = EMPLOYEES = [
    {"id": 1, "name": "Jenna Solis"},
    {"id": 2, "name": "Chris Adams"},
]


# def get_all_employees():
# return EMPLOYEES
def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.id locationId,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        """
        )

        # Initialize an empty list to hold all location representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            employee = Employee(
                row["id"], row["name"], row["location_id"], row["address"]
            )

            location = Location(
                row["locationId"], row["location_name"], row["location_address"]
            )
            employee.location = location.__dict__
            employees.append(employee.__dict__)

    return employees

    # def get_single_employee(id):
    requested_employee = None
    for employee in EMPLOYEES:
        if employee["id"] == id:
            requested_employee = employee
    return requested_employee


def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.id locationId,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        WHERE e.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        employee = Employee(
            data["id"], data["name"], data["location_id"], data["address"]
        )
        location = Location(
            data["locationId"], data["location_name"], data["location_address"]
        )
        employee.location = location.__dict__
        return employee.__dict__


def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee


def delete_employee(id):
    employee_index = -1

    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index

    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee


def get_employees_by_location(locationId):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        select
           e.id,
           e.name,
           e.location_id
        FROM employee e
        WHERE e.location_id = ?
""",
            (locationId,),
        )
        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row["id"],
                row["name"],
                row["location_id"],
            )
            employees.append(employee.__dict__)
    return employees
