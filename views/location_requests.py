import sqlite3
import json
from models import Location
from .animal_requests import get_animals_by_location
from .employee_requests import get_employees_by_location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        """)

        locations = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            location = Location(row['id'], row['name'], row['address'])

            locations.append(location.__dict__)

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        location = Location(data['id'], data['name'], data['address'])

        location_animals = get_animals_by_location(id)

        if location_animals:
            for animal in location_animals:
                if animal['location'] is None:
                    del animal['location']
                if animal['customer'] is None:
                    del animal['customer']

        location.animals = location_animals

        location_employees = get_employees_by_location(id)

        if location_employees:
            for employee in location_employees:
                if employee['location'] is None:
                    del employee['location']

        location.employees = location_employees

        return location.__dict__

def create_location(location):
    max_id = LOCATIONS[-1]["id"]

    new_id = max_id + 1

    location["id"] = new_id

    LOCATIONS.append(location)

    return location

def update_location(id, new_location):

    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:

            LOCATIONS[index] = new_location
            break

def delete_location(id):

    location_index = -1


    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:

            location_index = index


    if location_index >= 0:
        LOCATIONS.pop(location_index)
