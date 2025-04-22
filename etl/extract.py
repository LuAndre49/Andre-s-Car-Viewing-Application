import json
import os
from pathlib import Path

def extract_car_listings():
    # Compute absolute path to data/raw/cars.json
    PROJECT_ROOT = Path(__file__).resolve().parents[1]  # etl/
    raw_path = PROJECT_ROOT / "data" / "raw" / "cars.json"

    if not raw_path.exists():
        print(f"File not found: {raw_path}")
        return []

    with open(raw_path, 'r', encoding='utf-8-sig') as f:
        content = f.read().strip()
        if not content:
            print("Warning: cars.json is empty.")
            return []

        # Remove any BOM characters just in case
        content = content.replace('\ufeff', '')

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []
