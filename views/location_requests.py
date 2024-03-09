lOCATIONS = [
    {"id": 1, "name": "Nashville North", "address": "8422 Johnson Pike"},
    {"id": 2, "name": "Nashville South", "address": "209 Emory Drive"},
]


def get_all_locations():
    return lOCATIONS


def get_single_location(id):
    requested_location = None

    for location in lOCATIONS:
        if location["id"] == id:
            requested_location = location

    return requested_location


def create_location(location):
    max_id = lOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    lOCATIONS.append(location)
    return location


def delete_location(id):
    location_index = -1

    for index, location in enumerate(lOCATIONS):
        if location["id"] == id:
            location_index = index

    if location_index >= 0:
        lOCATIONS.pop(location_index)


def update_location(id, new_location):
    for index, location in enumerate(lOCATIONS):
        if location["id"] == id:
            lOCATIONS[index] = new_location
