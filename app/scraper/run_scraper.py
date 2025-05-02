import subprocess
import os

def run_scraper():
    # Go to the Scrapy project directory
    project_dir = os.path.join(os.path.dirname(__file__), 'carscraper')
    
    # Use the Scrapy command to start the spider
    subprocess.run(['scrapy', 'crawl', 'CarScraper'], cwd=project_dir)
