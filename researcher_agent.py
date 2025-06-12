import requests
from bs4 import BeautifulSoup
from newspaper import Article
import trafilatura
from langdetect import detect
import re
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import time

class ResearcherAgent:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def is_allowed(self, url):
        try:
            parsed_url = urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch("*", url)
        except Exception:
            return True

    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\u0600-\u06FF\u0750-\u077Fa-zA-Z0-9\s.,!?،؛؟]', '', text)
        return text.strip()

    def extract_with_newspaper(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception:
            return None

    def extract_with_trafilatura(self, url):
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(downloaded)
            return None
        except Exception:
            return None

    def extract_with_bs4(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            main_content = None
            for tag in ['article', 'main', 'div[class*="content"]', 'div[class*="post"]']:
                main_content = soup.select_one(tag)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.body
            
            return main_content.get_text()
        except Exception:
            return None

    def extract_content(self, url):
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL نامعتبر است. لطفاً یک URL معتبر وارد کنید.")

        if not self.is_allowed(url):
            raise PermissionError("این وب‌سایت اجازه scraping نمی‌دهد.")

        try:
            content = self.extract_with_newspaper(url)
            if content:
                return {'content': self.clean_text(content), 'source': 'newspaper3k'}

            content = self.extract_with_trafilatura(url)
            if content:
                return {'content': self.clean_text(content), 'source': 'trafilatura'}

            content = self.extract_with_bs4(url)
            if content:
                return {'content': self.clean_text(content), 'source': 'beautifulsoup4'}

            raise ValueError("نتوانستیم محتوای قابل استخراجی از این صفحه پیدا کنیم.")

        except requests.exceptions.ConnectionError:
            raise ConnectionError("خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید.")
        except requests.exceptions.Timeout:
            raise TimeoutError("زمان اتصال به سرور به پایان رسید. لطفاً دوباره تلاش کنید.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise PermissionError("دسترسی به این وب‌سایت مسدود شده است.")
            elif e.response.status_code == 404:
                raise FileNotFoundError("صفحه مورد نظر یافت نشد.")
            else:
                raise Exception(f"خطا در استخراج محتوا: {str(e)}")
        except Exception as e:
            raise Exception(f"خطا در استخراج محتوا: {str(e)}")