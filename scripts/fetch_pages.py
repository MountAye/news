import asyncio
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_rendered_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()
        return html

with open("./scripts/cache.txt", 'r', encoding='utf-8') as file:
    content = file.readlines()
for line in content:
    url = line.partition("：")[0]
    html = fetch_rendered_html(url)
    
    # # Using requests and BeautifulSoup
    # headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" }
    # res = requests.get(url, headers=headers, timeout=10)
    # html = res.text

    soup = BeautifulSoup(html, "html.parser")

    # Page title
    title = soup.title.string if soup.title else None

    # Meta tags
    meta = {
        tag.get("property") or tag.get("name"): tag.get("content")
        for tag in soup.find_all("meta")
        if tag.get("content")
    }

    print(line)
    print("Title:", title)
    print("Meta:", meta)

# This works as a script, but cannot run with jupyter because some sync/async issues.
