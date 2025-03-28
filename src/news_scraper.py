import os
import json
import requests
from bs4 import BeautifulSoup

class NewsScraper:
    def __init__(self, company: str):
        self.company = company
        self.headers = {"User-Agent": "Mozilla/5.0"}
        # self.output_dir = "news-articles"
        # os.makedirs(self.output_dir, exist_ok=True)
    
    def scrape_bbc_news(self):
        search_url = f"https://www.bbc.co.uk/search?q={self.company}"
        response = requests.get(search_url, headers=self.headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch search results"}
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a", href=True)
        article_links = [a["href"] for a in articles if "/news/articles/" in a["href"]][:7]
        
        results = []
        for article_url in article_links:
            if not article_url.startswith("https"):
                article_url = "https://www.bbc.com" + article_url
            
            article_response = requests.get(article_url, headers=self.headers)
            if article_response.status_code != 200:
                continue
            
            article_soup = BeautifulSoup(article_response.text, "html.parser")
            title = article_soup.find("h1").text.strip() if article_soup.find("h1") else "No Title Found"
            text_blocks = article_soup.find_all("div", {"data-component": "text-block"})
            text = "\n".join([p.text.strip() for block in text_blocks for p in block.find_all("p")])
            
            results.append({"title": title, "content": text, "source":"bbc_news"})
        
        return results
    
    def scrape_ap_news(self):
        search_url = f"https://apnews.com/search?q={self.company}"
        response = requests.get(search_url, headers=self.headers)
        if response.status_code != 200:
            return {"error": "Failed to fetch search results"}
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a", href=True)
        article_links = list(set([a["href"] for a in articles if "/article/" in a["href"] and self.company.lower() in a.text.lower()]))[:7]
        
        results = []
        for article_url in article_links:
            if not article_url.startswith("https"):
                article_url = "https://apnews.com" + article_url
            
            article_response = requests.get(article_url, headers=self.headers)
            if article_response.status_code != 200:
                continue
            
            article_soup = BeautifulSoup(article_response.text, "html.parser")
            title = article_soup.find("h1").text.strip() if article_soup.find("h1") else "No Title Found"
            text_blocks = article_soup.find_all("div", class_="RichTextStoryBody")
            text = "\n".join([p.text.strip() for block in text_blocks for p in block.find_all("p")])
            
            results.append({"title": title, "content": text, "source":"ap_news"})
        
        return results

def main(company: str):
    scraper = NewsScraper(company)
    bbc_articles = scraper.scrape_bbc_news()
    ap_articles = scraper.scrape_ap_news()
    articles = {"BBC": bbc_articles, "AP": ap_articles}
    return articles

if __name__ == "__main__":
    main()