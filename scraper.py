
import time
from urllib.parse import quote_plus, urlparse

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_dawn(keyword):

    options = Options()

    # Chromium browser location inside Docker
    options.binary_location = "/usr/bin/chromium"

    # Headless browser configuration
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # ChromeDriver location inside Docker
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    try:
        # Search DAWN News
        search_url = (
            "https://www.dawn.com/search?q="
            + quote_plus(keyword)
        )

        print("Searching DAWN for:", keyword)

        driver.get(search_url)

        # Wait for search results
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href*='/news/']")
            )
        )

        # Find the first actual news article
        links = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/news/']"
        )

        article_url = None

        for link in links:

            href = link.get_attribute("href")

            if not href:
                continue

            parsed = urlparse(href)

            if (
                parsed.hostname == "www.dawn.com"
                and parsed.path.startswith("/news/")
            ):
                article_url = href
                break

        if not article_url:
            raise Exception("No news article found.")

        print("First article:", article_url)

        # Open selected article
        driver.get(article_url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "h1")
            )
        )

        time.sleep(2)

        # Extract article HTML
        soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )

        # Extract article title
        heading = soup.find("h1")

        if not heading:
            raise Exception("Article title not found.")

        title = heading.get_text(" ", strip=True)

        # Extract article paragraphs
        content = soup.select(
            ".story__content p, article p, main p"
        )

        paragraphs = [
            p.get_text(" ", strip=True)
            for p in content
            if len(p.get_text(strip=True)) > 40
        ]

        article_text = "\n".join(paragraphs)

        if len(article_text) < 100:
            raise Exception(
                "Could not extract sufficient article text."
            )

        return {
            "title": title,
            "url": driver.current_url,
            "text": article_text
        }

    finally:
        # Always close the browser
        driver.quit()
