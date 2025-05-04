import sqlite3
from pathlib import Path

def create_connection():
    db_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "cars.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            price REAL,
            link TEXT,
            local_image_path TEXT,
            brand TEXT,
            model TEXT,
            year INTEGER,
            transmission TEXT,
            mileage TEXT,
            condition TEXT,
            fuel_type TEXT,
            location TEXT,
            image_url TEXT
        );
    ''')
    conn.commit()
    


def insert_data(conn, cars):
    cursor = conn.cursor()

    for car in cars:
        cursor.execute("""
            INSERT OR REPLACE INTO cars (
                title, price, link, image_url, local_image_path,
                brand, model, year, transmission, mileage,
                condition, fuel_type, location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            car["title"], car["price"], car["link"],
            car["image_url"], car["local_image_path"],
            car["brand"], car["model"], car["year"],
            car["transmission"], car["mileage"],
            car["condition"], car["fuel_type"], car["location"]
        ))
    conn.commit()

def load(transformed_data):
    conn = create_connection()
    create_table(conn)
    insert_data(conn, transformed_data)
    conn.close()
    
    print("[INFO] Data loaded into SQLite database.")
    print(f"[INFO] DB successfully created at {Path(__file__).resolve().parents[2] / 'data' / 'processed' / 'cars.db'}")
