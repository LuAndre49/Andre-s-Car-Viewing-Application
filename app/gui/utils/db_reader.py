import sqlite3
from pathlib import Path

def fetch_car_data():
    db_path = Path(__file__).resolve().parents[3] / "data" / "processed" / "cars.db"

    print(f"[DEBUG] DB path: {db_path}")  # Debug print

    if not db_path.exists():
        raise FileNotFoundError(f"[ERROR] Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT title, price, link, image_url, local_image_path, brand, model, year, transmission, mileage, condition, fuel_type, location FROM cars")
    rows = cursor.fetchall()
    conn.close()

    car_data = []
    for row in rows:
        car_data.append({
            "title": row[0],
            "price": row[1],
            "link": row[2],
            "image_url": row[3],
            "local_image_path": row[4],
            "brand": row[5],
            "model": row[6],
            "year": row[7],
            "transmission": row[8],
            "mileage": row[9],
            "condition": row[10],
            "fuel_type": row[11],
            "location": row[12],
        })
    return car_data
