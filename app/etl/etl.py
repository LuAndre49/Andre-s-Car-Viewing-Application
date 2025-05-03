from app.etl.extract import extract
from app.etl.transform import transform
from app.etl.load import load

def run_etl():
    listings, brands = extract(max_pages=1)
    transformed = transform(listings, list(brands))
    load(transformed)
