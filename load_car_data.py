import json
import os

def load_car_listings():
    filepath = 'scraper/carscraper/used_cars.json'

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read().strip()
        if not content:
            print("Warning: used_cars.json is empty.")
            return []

        # Remove any BOM characters just in case
        content = content.replace('\ufeff', '')

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []
