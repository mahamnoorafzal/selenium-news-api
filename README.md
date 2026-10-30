# DAWN News Automation API

## Project Information

- Registration Number: FA23-BDS-020
- News Source: DAWN News Pakistan
- Programming Language: Python
- Automation Tool: Selenium
- API Framework: Flask
- Containerization: Docker

## Project Description

This project uses Selenium to automate news extraction from DAWN News Pakistan. It accepts a keyword through a REST API, searches for relevant news articles, extracts article content, and generates a short summary.

## Technologies Used

- Python
- Selenium
- Chromium
- ChromeDriver
- Flask
- BeautifulSoup
- Docker

## Project Files

| File | Description |
|---|---|
| app.py | Flask REST API |
| scraper.py | Selenium news extraction |
| summarizer.py | Article summarization |
| requirements.txt | Python dependencies |
| Dockerfile | Docker configuration |

## API Endpoint

Method: GET

Endpoint: /get?keyword=AI

Example:

http://localhost:7000/get?keyword=AI

## Expected JSON Response

{
  "registration": "FA23-BDS-020",
  "newssource": "DAWN News Pakistan",
  "keyword": "AI",
  "url": "ARTICLE_URL",
  "summary": "Article summary appears here."
}

## Docker Commands

Build image:

docker build -t selenium-news-api:1.0 .

Run container:

docker run -d --name selenium-news-api -p 7000:7000 selenium-news-api:1.0

## Note

During AWS EC2 testing, DAWN returned HTTP 403 due to Cloudflare security verification. Docker deployment and the Flask homepage were successful.
