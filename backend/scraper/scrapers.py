"""
Scholarship scraping module using BeautifulSoup and Selenium
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime
from dateutil import parser
import re
from .models import ScrapingLog
from scholarships.models import Scholarship
import pymongo
from django.conf import settings


class ScholarshipScraper:
    """Base scraper class for scholarships"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.mongo_client = None
        self.mongo_db = None
        self._init_mongodb()
    
    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            mongodb_settings = settings.MONGODB_SETTINGS
            if mongodb_settings.get('username') and mongodb_settings.get('password'):
                connection_string = f"mongodb://{mongodb_settings['username']}:{mongodb_settings['password']}@{mongodb_settings['host']}:{mongodb_settings['port']}/{mongodb_settings['db']}"
            else:
                connection_string = f"mongodb://{mongodb_settings['host']}:{mongodb_settings['port']}"
            
            self.mongo_client = pymongo.MongoClient(connection_string)
            self.mongo_db = self.mongo_client[mongodb_settings['db']]
            print("MongoDB connection established")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.mongo_client = None
            self.mongo_db = None
    
    def _get_selenium_driver(self, headless=True):
        """Get Selenium WebDriver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"Error creating Selenium driver: {e}")
            return None
    
    def _parse_date(self, date_string):
        """Parse date string to datetime object"""
        if not date_string:
            return None
        
        try:
            # Try parsing with dateutil
            return parser.parse(date_string).date()
        except:
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y']:
                try:
                    return datetime.strptime(date_string, fmt).date()
                except:
                    continue
        return None
    
    def _extract_amount(self, text):
        """Extract funding amount from text"""
        if not text:
            return ""
        
        # Look for currency patterns
        patterns = [
            r'\$[\d,]+(?:\.\d+)?',
            r'[\d,]+(?:\.\d+)?\s*(?:USD|EUR|GBP)',
            r'up to \$[\d,]+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return ""
    
    def _store_raw_data(self, scholarship_data):
        """Store raw scraped data in MongoDB"""
        if not self.mongo_db:
            return None
        
        try:
            collection = self.mongo_db['raw_scholarships']
            result = collection.insert_one(scholarship_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error storing raw data in MongoDB: {e}")
            return None
    
    def _check_duplicate(self, title, link):
        """Check if scholarship already exists"""
        if link:
            return Scholarship.objects.filter(link=link).exists()
        return Scholarship.objects.filter(title=title).exists()
    
    def scrape_scholarship(self, url):
        """Scrape a single scholarship page (to be implemented by subclasses)"""
        raise NotImplementedError
    
    def scrape_all(self):
        """Scrape all scholarships from source (to be implemented by subclasses)"""
        raise NotImplementedError


class GenericScholarshipScraper(ScholarshipScraper):
    """Generic scraper for static HTML pages"""
    
    def scrape_scholarship(self, url):
        """Scrape a single scholarship from URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information (generic patterns)
            title = soup.find('h1') or soup.find('title')
            title = title.get_text(strip=True) if title else "Untitled Scholarship"
            
            # Try to find description
            description = ""
            for tag in soup.find_all(['p', 'div']):
                text = tag.get_text(strip=True)
                if len(text) > 100:
                    description = text
                    break
            
            # Store raw data
            raw_data = {
                'url': url,
                'title': title,
                'description': description,
                'html': str(soup),
                'scraped_at': datetime.now().isoformat()
            }
            mongo_id = self._store_raw_data(raw_data)
            
            return {
                'title': title,
                'description': description,
                'link': url,
                'source_url': url,
                'mongo_id': mongo_id
            }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None


class SeleniumScholarshipScraper(ScholarshipScraper):
    """Scraper using Selenium for dynamic content"""
    
    def scrape_scholarship(self, url):
        """Scrape a single scholarship using Selenium"""
        driver = self._get_selenium_driver()
        if not driver:
            return None
        
        try:
            driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            # Extract information
            title = driver.find_element(By.TAG_NAME, 'h1').text if driver.find_elements(By.TAG_NAME, 'h1') else "Untitled"
            
            description = ""
            try:
                description_elem = driver.find_element(By.CLASS_NAME, 'description')
                description = description_elem.text
            except NoSuchElementException:
                pass
            
            # Store raw data
            raw_data = {
                'url': url,
                'title': title,
                'description': description,
                'html': driver.page_source,
                'scraped_at': datetime.now().isoformat()
            }
            mongo_id = self._store_raw_data(raw_data)
            
            return {
                'title': title,
                'description': description,
                'link': url,
                'source_url': url,
                'mongo_id': mongo_id
            }
        except Exception as e:
            print(f"Error scraping {url} with Selenium: {e}")
            return None
        finally:
            driver.quit()


def scrape_mock_scholarships():
    """Generate mock scholarships for testing"""
    mock_scholarships = []
    
    titles = [
        "Global Excellence Scholarship",
        "Tech Innovation Grant",
        "Women in Engineering Scholarship",
        "International Student Merit Award",
        "STEM Research Fellowship",
        "Business Leadership Scholarship",
        "Arts and Culture Grant",
        "Healthcare Excellence Award",
        "Environmental Science Scholarship",
        "Social Impact Fellowship"
    ]
    
    organizations = [
        "International Education Foundation",
        "Future Tech Foundation",
        "Engineering Excellence Society",
        "Global Education Network",
        "STEM Research Institute",
        "Business Leaders Association",
        "Arts Council International",
        "Healthcare Professionals Network",
        "Environmental Research Center",
        "Social Change Foundation"
    ]
    
    countries = ["United States", "Canada", "Australia", "United Kingdom", "Germany", "France"]
    
    for i, title in enumerate(titles):
        mock_scholarships.append({
            'title': title,
            'organization': organizations[i],
            'description': f"Merit-based scholarship for outstanding students in {title.split()[0]} fields.",
            'eligibility': "GPA 3.5+, TOEFL 100+, relevant field of study",
            'deadline': None,  # Will be set randomly
            'country': countries[i % len(countries)],
            'funding_amount': f"${(i+1)*5000:,}",
            'link': f"https://example.com/scholarship/{i+1}",
            'source_url': f"https://example.com/scholarships",
        })
    
    return mock_scholarships

