import scrapy
import re
from urllib.parse import urljoin

class UsedCarScraper(scrapy.Spider):
    name = 'usedCarScraper'
    allowed_domains = ['philkotse.com']
    start_urls = ['https://philkotse.com/used-cars-for-sale']
    max_pages = 50  # Adjust as needed
    custom_settings = {
        'FEEDS': {
            'used_cars.csv': {
                'format': 'csv',
                'encoding': 'utf-8-sig',
                'overwrite': True
            }
        }
    }
    def parse(self, response):
        
        if 'e/p' in response.url:
            current_page = int(response.url.split('/p')[-1])  # extract page number
        else:
            current_page = 1  # The first page does not contain '/p'

        self.logger.info(f"Parsing page {current_page}")


        listings = response.css('div.row.listitempage div.col-4')
        
        for car in listings:
            # Sometimes, the transmission is stated in the named, not in a li element....
            title = car.css('h3.title a::text').get().strip()
            transmission = car.css('li[data-tag="transmission"]::text').get()
            if not transmission and title:
                # Regex to find words like "Automatic" or "Manual" in the title
                transmission = self.extract_transmission_from_title(title)



            yield {
                'title': title,
                'price': car.css('div.price::text').get(default='').strip(),
                'location': car.css('div.location::text').get(default='').strip(),
                'transmission': transmission,
                'year': car.css('ul.tag li:nth-child(2)::text').get(),
                'mileage': car.css('li[data-tag="numOfKm"]::text').get(),
                'status': car.css('li.label-used::text').get(),
                'link': urljoin(response.url, car.css('a::attr(href)').get()),
                'image': car.css('img::attr(data-src)').get()

            }

        if current_page < self.max_pages:
            # If we're on the first page, the next page should be '/p2'
            if current_page == 1:
                next_url = "https://philkotse.com/used-cars-for-sale/p2"
            else:
                next_url = f"https://philkotse.com/used-cars-for-sale/p{current_page + 1}"

            yield scrapy.Request(url=next_url, callback=self.parse)
    def extract_transmission_from_title(self, title):
        """Extract transmission type from the title using regex."""
        match = re.search(r'\b(Automatic|Manual)\b', title, re.IGNORECASE)
        return match.group(0) if match else None
