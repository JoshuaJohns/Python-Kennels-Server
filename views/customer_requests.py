CUSTOMERS = [
    {"id": 1, "name": "Ryan Tan"},
    {"id": 2, "name": "Jack Black"},
    {"id": 3, "name": "Blake Real"},
]


def get_all_customers():
    return CUSTOMERS


def get_single_customer(id):
    requested_customer = None
    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = customer
    return requested_customer
