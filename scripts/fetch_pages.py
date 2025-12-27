import json
import yaml
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

def read_x(link,soup):
    info = { "url": link }

    meta = soup.title.string
    author,_,rest = meta.partition(' on X: "')
    content,_,_   = rest.rpartition('" / X')
    content,_,_   = content.rpartition("https://t.co/")

    tag = soup.select_one('.r-12kyg2d time')
    if tag:
        info["date"] = tag.get("datetime").strip()

    info["text"] = ' '.join(content.strip().split())
    info["author"] = f"Twitter@{author.strip()}"
    return info

def read_zaobao(link,soup):
    info = read_default(link,soup)
    info["author"] = "联合早报"
    info['date'] = "NOT FOUND" # how do I find the div immediately after h1 of article, and get the div inside with a span, and then get the content after the span?
    h1 = soup.find('article h1')
    if h1:
        div = h1.find_next_sibling('div')
        if div:
            span = div.find('span')
            if span:
                parent = span.get_parent()
                if parent:
                    info['date'] = parent.get_text().replace("发布/",'').replace(" ",'T').replace("年",'-').replace('月','-').replace('日','-')
    return info

def read_youtube(link,soup):
    """need to append user name to site name"""
    raise NotImplementedError
def read_bilibili(link,soup):
    """
    1. cannot find site_name and user name.
    2. fetched date is not in correct format.
    """
    raise NotImplementedError

def read_default(link,soup):

    def get_publish_date(soup):
        # Try Open Graph article:published_time (common for social sharing)
        tag = soup.find('meta', attrs={'property': 'article:published_time'})
        if tag:
            return tag.get('content')
        
        # Try schema.org datePublished (often in JSON-LD, but can be in meta)
        tag = soup.find('meta', attrs={'itemprop': 'datePublished'})
        if tag:
            return tag.get('content')
        
        # Try generic 'publishdate' or 'date' meta names
        tag = soup.find('meta', attrs={'name': 'publishdate'})
        if tag:
            return tag.get('content')
        
        tag = soup.find('meta', attrs={'name': 'date'})
        if tag:
            return tag.get('content')

        # Try JSON-LD structured data
        script = soup.find('script', type='application/ld+json')
        if script:
            try:
                data = json.loads(script.string)
                # Handle both single object and array of objects
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') in ['Article', 'NewsArticle', 'BlogPosting']:
                            date = item.get('datePublished')
                            if date:
                                return date
                elif isinstance(data, dict) and data.get('@type') in ['Article', 'NewsArticle', 'BlogPosting']:
                    date = data.get('datePublished')
                    if date:
                        return date
            except (json.JSONDecodeError, KeyError):
                pass  # Ignore parsing errors

        return None

    info = { "url": link }
    tag = soup.find('meta', attrs={'property': 'og:url'} )
    if tag:
        info['url'] = tag.get("content").strip()

    info["text"] = ' '.join((soup.title.string if soup.title else "[TITLE NOT FOUND]").split())
    tag = soup.find('meta', attrs={'property': 'og:title'} )
    if tag:
        info['text'] = ' '.join(tag.get("content").strip().split())

    tag = soup.find('meta', attrs={'property': 'og:site_name'} )
    if tag:
        info['author'] = tag.get("content").strip()

    date = get_publish_date(soup)
    if date:
        info['date'] = date.strip()

    tag = soup.find("meta", attrs={"name": "og:description"})
    if tag:
        info["details"] = [{ "text": tag.get("content").strip() }]

    return info


if __name__ == "__main__":
    with open("./cache/links.txt", 'r', encoding='utf-8') as file:
        content = file.readlines()

    yaml_data = []
    for line in content:
        url = line.partition("：")[0].strip()
        html = fetch_rendered_html(url)

        # # Using requests and BeautifulSoup
        # headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" }
        # res = requests.get(url, headers=headers, timeout=10)
        # html = res.text

        soup = BeautifulSoup(html, "html.parser")

        if "https://x.com" in url:
            info = read_x(url, soup)
        else:
            info = read_default(url, soup)
        
        yaml.dump( 
            [info], 
            stream=open("cache/draft.yml",'a',encoding='utf-8'), 
            indent=2, width=None,
            encoding='utf-8', allow_unicode=True 
        )
        print(url.strip())

# This works as a script, but cannot run in jupyter because of some sync/async issues.
