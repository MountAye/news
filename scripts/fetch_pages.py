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

    break
# This works as a script, but cannot run with jupyter because some sync/async issues.


# {
#     'viewport': 'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=0,viewport-fit=cover', 
#           None: 'A8o5T4MyEkRZqLA9WeG2XTFdV5tsX2Prg85xyQ+RL1btVuybB1K/EQ+7JUsPK+J32oBMTnsoF9B4A+qTlL6efgQAAABweyJvcmlnaW4iOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb206NDQzIiwiZmVhdHVyZSI6IkZlZENtQnV0dG9uTW9kZSIsImV4cGlyeSI6MTc0NDY3NTIwMCwiaXNUaGlyZFBhcnR5Ijp0cnVlfQ==', 
#    'fb:app_id': '2231777543', 
# 'og:site_name': 'X (formerly Twitter)', 
# 'google-site-verification': 'reUF-TgZq93ZGtzImw42sfYglI2hY0QiGRmfc4jeKbs', 
# 'facebook-domain-verification': 'x6sdcc8b5ju3bh8nbm59eswogvg6t1', 
# 'twitter-site-verification': 'yy2VpVVpR8TdxbcOrV6HveUHeicv+UIsbpCFXHUsEhb4pHuEmdCiah/GLi7j0uJg', 
#  'theme-color': '#000000', 
#     'og:image': 'https://abs.twimg.com/rweb/ssr/default/v2/og/image.png', 
#     'og:title': '冰玉IceJade🇺🇦# #StandWithUkraine on X: "关恒要被美国送到乌干达了。\n自由女神暗淡无光。\n这就是白川粉，华川粉，民运川粉支持川普带来的恶果之一。 https://t.co/CkGyWPr0Jr" / X'
# }