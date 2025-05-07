import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
from pathlib import Path

car_URLS = {
    "New":  "https://www.autodeal.com.ph/cars/search?sort-by=alphabetical&page={}",
    "Used": "https://www.autodeal.com.ph/used-cars/search/certified-pre-owned+repossessed+used-car-status/page-{}?sort-by=relevance"
}

def extract_cars(max_pages=1):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    listings = []
    brands = set()
    old_brand_loaded = False  # flag to prevent re-clicking brand toggle
    new_brand_loaded = False  # flag to prevent re-clicking brand toggle
    try:
        for condition, base_url in car_URLS.items():
            for page in range(1, max_pages + 1):
                url = base_url.format(page)
                print(f"[INFO] Loading {condition} page {page}: {url}")
                driver.get(url)
                time.sleep(3)

                if condition == "New":
                    card_selector = "article.card.simple.vertical"
                else:
                    card_selector = "article.card.withshadow.listing-featured"

                cards = driver.find_elements(By.CSS_SELECTOR, card_selector)
                if not cards:
                    print(f"[WARN] No listings found on {url}")
                    continue

                for card in cards:
                    try:
                        listing = {"condition": condition}

                        if condition == "New":
                            listing["title"] = card.find_element(By.CSS_SELECTOR, "h5 a").text.strip()
                            listing["price"] = card.find_element(By.CSS_SELECTOR, "div.display-flex span").text.strip()
                            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            image = card.find_element(By.CSS_SELECTOR, "img")
                            listing["image_url"] = image.get_attribute("data-src") or image.get_attribute("src")
                            listing["link"] = f"https://www.autodeal.com.ph{link}" if link.startswith("/") else link
                        else:
                            listing["title"] = card.find_element(By.CSS_SELECTOR, "h3").text.strip()
                            listing["price"] = card.find_element(By.CSS_SELECTOR, "h4").text.strip()
                            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            image = card.find_element(By.CSS_SELECTOR, "div.image-container img")
                            listing["image_url"] = image.get_attribute("data-src") or image.get_attribute("src")
                            listing["link"] = f"https://www.autodeal.com.ph{link}" if link.startswith("/") else link
                            listing["location"] = card.find_element(By.CSS_SELECTOR, "span.locality small").text.strip()

                            stats = card.find_elements(By.CSS_SELECTOR, "span.small.reducedopacity")
                            listing["mileage"] = stats[0].text.strip() if len(stats) > 0 else ""
                            listing["transmission"] = stats[1].text.strip() if len(stats) > 1 else ""
                            listing["fuel_type"] = stats[2].text.strip() if len(stats) > 2 else ""

                        listings.append(listing)

                    except Exception as e:
                        print(f"[WARN] Skipping a {condition} car due to error: {e}")

                if not new_brand_loaded and condition == 'New':
                    try:
                        
                        show_all_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Show All Car Make')]")
                        if show_all_buttons:
                            driver.execute_script("arguments[0].click();", show_all_buttons[0])
                            time.sleep(2)
                        else:
                            print(f"[WARN] No 'Show All Car Make' button found on {url}")
                        brand_ul = driver.find_element(By.CSS_SELECTOR, "ul.options.nostyle.nopad.nomargin.display-flex")
                        brand_items = brand_ul.find_elements(By.TAG_NAME, "li")

                        if not brand_items:
                            print(f"[WARN] No brand items found in container on {url}")
                        else:
                            for brand in brand_items:
                                try:
                                    brand_name = brand.find_element(By.CSS_SELECTOR, "label").text.strip()
                                    if brand_name:
                                        brands.add(brand_name)
                                        #print(f"[INFO] Found brand: {brand_name}")
                                except Exception as e:
                                    print(f"[WARN] Skipped brand item due to error: {e}")
                        
                        new_brand_loaded = True
                
                    except Exception as e:
                        print(f"[ERROR] Brand scrape error: {e}")

                elif not old_brand_loaded and condition == 'Used':
                    try:
                        brand_ul = driver.find_element(By.CSS_SELECTOR, "div#car-make-filter-list")
                        brand_items = brand_ul.find_elements(By.TAG_NAME, "input")
                        if not brand_items:
                            print(f"[WARN] No brand items found in container on {url}")
                        else:
                            for brand in brand_items:
                                try:
                                    brand_name = brand.get_attribute("data-name").strip()
                                    if brand_name:
                                        brands.add(brand_name)
                                        #print(f"[INFO] Found brand: {brand_name}")
                                except Exception as e:
                                    print(f"[WARN] Skipped brand item due to error: {e}")
                        new_brand_loaded = True
                    except Exception as e:
                        print(f"[ERROR] Brand scrape error: {e}")
                else:
                    continue
                time.sleep(1)

    finally:
        driver.quit()
    
    try:
        with open(str(Path(__file__).parent.parent.parent / "data/raw/listings.json"), "w") as f:
            json.dump(listings, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to write listings to file: {e}")

    try:
        with open(str(Path(__file__).parent.parent.parent / "data/raw/brands.json"), "w") as f:
            json.dump(list(brands), f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to write brands to file: {e}")

    return listings, brands

def extract_news():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    news = []
    try:
        url = "https://www.autodeal.com.ph/articles/latest-stories"
        print(f"[INFO] Loading news page: {url}")
        driver.get(url)
        time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, "li.padtop20.padbottom20.row.gutters.card.directory-listing")
        if not cards:
            print(f"[WARN] No news found on {url}")
            return news

        for card in cards:
            try:
                image_container = card.find_element(By.CSS_SELECTOR, "div.col.span_3")
                image = image_container.find_element(By.TAG_NAME, "img")
                image_url = image.get_attribute("data-src") or image.get_attribute("src")
                title_container = card.find_element(By.CSS_SELECTOR, "h3.h5.nomargin.bold.marginright50")
                title_a = title_container.find_element(By.TAG_NAME, "a")
                title = title_a.text.strip()
                link = title_a.get_attribute("href")
                category = title_a.get_attribute("data-gacategory")

                author_container = card.find_element(By.CSS_SELECTOR, "div.byline")
                author_a = author_container.find_element(By.TAG_NAME, "a")
                author = author_a.find_elements(By.TAG_NAME, "span")[0].text.strip()
                date = author_a.find_elements(By.TAG_NAME, "span")[1].text.strip()

                intro = card.find_element(By.CSS_SELECTOR, "p").text.strip()

                news.append({
                    "title": title,
                    "link": link,
                    "image_url": image_url,
                    "date": date,
                    "author": author,
                    "category": category,
                    "intro": intro
                })
            except Exception as e:
                print(f"[WARN] Skipping a news item due to error: {e}")

    finally:
        driver.quit()

    try:
        with open(str(Path(__file__).parent.parent.parent / "data/raw/news.json"), "w") as f:
            json.dump(news, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to write news to file: {e}")

    return news