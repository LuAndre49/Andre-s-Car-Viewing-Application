import os
import json
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path

def download_image(url, save_dir="data/images"):
    try:
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(save_dir, filename)

        if not os.path.exists(filepath):
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
        return filepath
    except Exception as e:
        print(f"[Image Download Error] {url}: {e}")
        return None

def transform(raw_listings, car_brands):
    transformed = []
    for car in raw_listings:
        title = car.get('title', '')
        brand = extract_brand(title, car_brands)
        year = extract_year(title)
        model = extract_model(title, brand)

        raw_price = car.get('price', '')

        normalized = raw_price.replace('₱', '').replace('P', '').replace(',', '').strip()
        
        normalized = normalized.replace('–', '-')

        if normalized.upper() == 'PRICE ON REQUEST':
            price = None
        elif normalized.isdigit():
            price = int(normalized)
        elif '-' in normalized:
            parts = [p.strip() for p in normalized.split('-')]
            nums = [int(p) for p in parts if p.isdigit()]
            price = sum(nums) // len(nums) if nums else None
        else:
            price = None

        image_url = car.get('image_url')
        local_image_path = download_image(image_url) if image_url else ""

        transmission = car.get('transmission')
        fuel_type = car.get('fuel_type')
        mileage = car.get('mileage', 'Not applicable')
        location = car.get('location', '')

        if car['condition'] == 'New':
            year, trans, fuel, location = fetch_new_car_details(car['link'])
            transmission = transmission or trans
            fuel_type = fuel_type or fuel
            mileage = 'Not applicable'
        else:
            mileage = mileage.replace('km', '').replace(',', '').strip()

        transformed.append({
            'title': title,
            'price': price,
            'link': car.get('link', ''),
            'image_url': image_url,
            'local_image_path': local_image_path,
            'brand': brand or '',
            'model': model or '',
            'year': year or '',
            'transmission': transmission or '',
            'mileage': mileage,
            'fuel_type': fuel_type or '',
            'condition': car.get('condition', ''),
            'location': location
        })

    return transformed

def extract_brand(title, car_brands):
    for brand in car_brands:
        if brand.lower() in title.lower():
            return brand
    return None

def extract_year(title):
    match = re.search(r'\b(20\d{2})\b', title)
    if match:
        return match.group(1)
    return None

def extract_model(title, brand):
    if brand:
        pattern = re.compile(re.escape(brand), re.IGNORECASE)
        model = pattern.sub('', title).strip()
        return model
    return title

def fetch_new_car_details(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        year = None
        title_tag = soup.select_one("header h1")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            match = re.search(r"\b(19|20)\d{2}\b", title_text)
            if match:
                year = match.group(0)

        transmission = None
        fuel_type = None
        specs_rows = soup.select("#specs-table-tab tr")
        for row in specs_rows:
            cols = row.find_all('td')
            if len(cols) != 2:
                continue
            label = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            if 'Transmission' in label:
                transmission = value
            elif 'Fuel Type' in label:
                fuel_type = value

        location = None
        location_article = soup.select_one("article.dealer-listing p.small")
        if location_article:
            location = location_article.get_text(strip=True)

        return year, transmission, fuel_type, location
    except Exception as e:
        print(f"[ERROR] Failed to fetch details from {url}: {e}")
        return None, None, None
