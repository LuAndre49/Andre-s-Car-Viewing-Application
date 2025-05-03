import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

URLS = {
    "New":  "https://www.autodeal.com.ph/cars/search?sort-by=alphabetical&page={}",
    "Used": "https://www.autodeal.com.ph/used-cars/search/certified-pre-owned+repossessed+used-car-status/page-{}?sort-by=relevance"
}

def extract(max_pages=1):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    listings = []
    brands = set()
    brand_loaded = False  # flag to prevent re-clicking brand toggle

    try:
        for condition, base_url in URLS.items():
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

                        listings.append(listing)

                    except Exception as e:
                        print(f"[WARN] Skipping a {condition} car due to error: {e}")

                # Only load brand list once (shared sidebar)
                if not brand_loaded:
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
                        brand_loaded = True

                    except Exception as e:
                        print(f"[ERROR] Brand scrape error: {e}")

                time.sleep(1)

    finally:
        driver.quit()

    return listings, brands
