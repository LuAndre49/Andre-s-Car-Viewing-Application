import sqlite3
from pathlib import Path

def fetch_car_data():
    db_path = Path(__file__).resolve().parents[3] / "data" / "processed" / "cars.db"

    print(f"[DEBUG] DB path: {db_path}")  # Debug print

    if not db_path.exists():
        raise FileNotFoundError(f"[ERROR] Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT title, price, brand, model, year, transmission, mileage, condition, image_url FROM cars")
    rows = cursor.fetchall()
    conn.close()

    car_data = []
    for row in rows:
        car_data.append({
            "title": row[0],
            "price": row[1],
            "brand": row[2],
            "model": row[3],
            "year": row[4],
            "transmission": row[5],
            "mileage": row[6],
            "condition": row[7],
            "image_url": row[8],
        })
    return car_data
