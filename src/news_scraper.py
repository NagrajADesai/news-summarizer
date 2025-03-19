import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import random
from urllib.parse import quote
import os

class NewsArticleScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }
        # List of news sources with updated selectors
        self.news_sources = [
            {"url": "https://news.google.com/search?q={}&hl=en-US&gl=US&ceid=US:en", "type": "google_news"},
            {"url": "https://economictimes.indiatimes.com/searchresult.cms?query={}", "type": "economic_times"},
            {"url": "https://finance.yahoo.com/quote/{}/news", "type": "yahoo_finance"},
            {"url": "https://www.ndtv.com/search?searchtext={}", "type": "ndtv"}
        ]
    
    def clean_text(self, text):
        if not text:
            return ""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_date(self, date_str):
        try:
            # Handle common date formats
            date_str = self.clean_text(date_str)
            if not date_str:
                return None
                
            # Try to parse various date formats
            date_formats = [
                "%Y-%m-%d",
                "%d %b %Y", 
                "%B %d, %Y",
                "%d/%m/%Y",
                "%m/%d/%Y"
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
            
            # If no format matches, return the original string
            return date_str
        except:
            return None
    
    def scrape_google_news(self, soup):
        articles = []
        print("Attempting to scrape Google News...")
        
        # Save the HTML for debugging
        with open("google_news_debug.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        
        # Try different selectors
        selectors = [
            "article",
            ".DBQmFf",
            ".NiLAwe",
            ".lBwEZb",
            ".h4VLc"
        ]
        
        for selector in selectors:
            article_elements = soup.select(selector)
            print(f"Found {len(article_elements)} elements with selector '{selector}'")
            
            if len(article_elements) > 0:
                break
        
        if len(article_elements) == 0:
            print("No articles found in Google News. Trying alternative approach.")
            # Fall back to a more general approach
            article_elements = soup.find_all("div", class_=lambda x: x and ("NiLAwe" in x or "lBwEZb" in x))
            print(f"Found {len(article_elements)} elements with alternative approach")
        
        for i, article in enumerate(article_elements[:20]):
            try:
                # Extract title - try multiple selectors
                title_element = article.select_one("h3 a, h4 a, a[data-n-tid]")
                if not title_element:
                    title_element = article.find("a", class_=lambda x: x and "DY5T1d" in x)
                
                if not title_element:
                    continue
                
                title = self.clean_text(title_element.text)
                if not title:
                    continue
                
                # Extract summary
                summary_element = article.select_one("h4, .Rai5ob, .xBbh9")
                summary = self.clean_text(summary_element.text) if summary_element else ""
                
                # Extract source
                source_element = article.select_one("div[data-n-tid] a, .wEwyrc, .SVJrMe")
                source = self.clean_text(source_element.text) if source_element else ""
                
                # Extract date
                time_element = article.select_one("time, .WW6dff")
                published_date = time_element.get("datetime") if time_element and time_element.has_attr("datetime") else None
                if not published_date and time_element:
                    published_date = self.clean_text(time_element.text)
                
                # Get link
                link = ""
                if title_element.has_attr("href"):
                    link_element = title_element["href"]
                    if link_element.startswith("/"):
                        link = "https://news.google.com" + link_element
                    else:
                        link = link_element
                
                if title:
                    articles.append({
                        "title": title,
                        "summary": summary,
                        "source": source,
                        "published_date": published_date,
                        "url": link,
                        "scraper_source": "google_news"
                    })
                
                print(f"Found article {i+1}: {title[:50]}...")
                
                if len(articles) >= 10:
                    break
                    
            except Exception as e:
                print(f"Error parsing Google News article {i+1}: {e}")
                continue
        
        print(f"Successfully scraped {len(articles)} articles from Google News")
        return articles
    
    def scrape_economic_times(self, soup):
        articles = []
        print("Attempting to scrape Economic Times...")
        
        article_elements = soup.select(".article, .eachStory")
        print(f"Found {len(article_elements)} elements with selector '.article, .eachStory'")
        
        for i, article in enumerate(article_elements[:15]):
            try:
                # Extract title
                title_element = article.select_one("h3 a, h2 a, .title a")
                if not title_element:
                    continue
                    
                title = self.clean_text(title_element.text)
                
                # Extract summary
                summary_element = article.select_one(".abstract, .desc")
                summary = self.clean_text(summary_element.text) if summary_element else ""
                
                # Extract date
                date_element = article.select_one(".date-format, .date")
                published_date = self.extract_date(date_element.text) if date_element else None
                
                # Extract link
                link = title_element.get("href") if title_element else None
                if link and not link.startswith("http"):
                    link = "https://economictimes.indiatimes.com" + link
                
                articles.append({
                    "title": title,
                    "summary": summary,
                    "source": "Economic Times",
                    "published_date": published_date,
                    "url": link,
                    "scraper_source": "economic_times"
                })
                
                print(f"Found article {i+1}: {title[:50]}...")
                
                if len(articles) >= 10:
                    break
                    
            except Exception as e:
                print(f"Error parsing Economic Times article {i+1}: {e}")
                continue
        
        print(f"Successfully scraped {len(articles)} articles from Economic Times")
        return articles
    
    def scrape_yahoo_finance(self, soup):
        articles = []
        print("Attempting to scrape Yahoo Finance...")
        
        article_elements = soup.select("li.js-stream-content")
        print(f"Found {len(article_elements)} elements with selector 'li.js-stream-content'")
        
        for i, article in enumerate(article_elements[:15]):
            try:
                # Extract title
                title_element = article.select_one("h3")
                if not title_element:
                    continue
                    
                title = self.clean_text(title_element.text)
                
                # Extract summary
                summary_element = article.select_one("p")
                summary = self.clean_text(summary_element.text) if summary_element else ""
                
                # Extract source and date
                source_element = article.select_one(".C(#959595)")
                source_text = self.clean_text(source_element.text) if source_element else ""
                source = source_text.split('·')[0].strip() if '·' in source_text else source_text
                
                published_date = None
                if '·' in source_text:
                    date_part = source_text.split('·')[1].strip()
                    published_date = self.extract_date(date_part)
                
                # Extract link
                link_element = article.select_one("a")
                link = link_element.get("href") if link_element else None
                if link and not link.startswith("http"):
                    link = "https://finance.yahoo.com" + link
                
                articles.append({
                    "title": title,
                    "summary": summary,
                    "source": source or "Yahoo Finance",
                    "published_date": published_date,
                    "url": link,
                    "scraper_source": "yahoo_finance"
                })
                
                print(f"Found article {i+1}: {title[:50]}...")
                
                if len(articles) >= 10:
                    break
                    
            except Exception as e:
                print(f"Error parsing Yahoo Finance article {i+1}: {e}")
                continue
        
        print(f"Successfully scraped {len(articles)} articles from Yahoo Finance")
        return articles
    
    def scrape_ndtv(self, soup):
        articles = []
        print("Attempting to scrape NDTV...")
        
        article_elements = soup.select(".news_Itm")
        print(f"Found {len(article_elements)} elements with selector '.news_Itm'")
        
        for i, article in enumerate(article_elements[:15]):
            try:
                # Extract title
                title_element = article.select_one(".newsHdng")
                if not title_element:
                    continue
                    
                title = self.clean_text(title_element.text)
                
                # Extract summary
                summary_element = article.select_one(".newsCont")
                summary = self.clean_text(summary_element.text) if summary_element else ""
                
                # Extract date
                date_element = article.select_one(".posted-on")
                published_date = self.extract_date(date_element.text) if date_element else None
                
                # Extract link
                link_element = title_element.find("a") if title_element else None
                link = link_element.get("href") if link_element else None
                
                articles.append({
                    "title": title,
                    "summary": summary,
                    "source": "NDTV",
                    "published_date": published_date,
                    "url": link,
                    "scraper_source": "ndtv"
                })
                
                print(f"Found article {i+1}: {title[:50]}...")
                
                if len(articles) >= 10:
                    break
                    
            except Exception as e:
                print(f"Error parsing NDTV article {i+1}: {e}")
                continue
        
        print(f"Successfully scraped {len(articles)} articles from NDTV")
        return articles
    
    def get_articles_for_company(self, company_name, num_articles=10):
        all_articles = []
        
        # Try each news source until we have enough articles
        for source in self.news_sources:
            if len(all_articles) >= num_articles:
                break
            
            # Format URL with company name
            url = source["url"].format(quote(company_name))
            
            try:
                print(f"\nScraping {url}")
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Choose appropriate scraping method based on source type
                    if source["type"] == "google_news":
                        articles = self.scrape_google_news(soup)
                    elif source["type"] == "economic_times":
                        articles = self.scrape_economic_times(soup)
                    elif source["type"] == "yahoo_finance":
                        articles = self.scrape_yahoo_finance(soup)
                    elif source["type"] == "ndtv":
                        articles = self.scrape_ndtv(soup)
                    else:
                        articles = []
                    
                    # Add new articles to our collection
                    for article in articles:
                        # Check for duplicates by title similarity
                        if not any(self.is_similar_title(article["title"], existing["title"]) for existing in all_articles):
                            all_articles.append(article)
                    
                    print(f"Total unique articles so far: {len(all_articles)}")
                    
                    # Break if we have enough articles
                    if len(all_articles) >= num_articles:
                        break
                        
                    # Be nice to the servers
                    time.sleep(random.uniform(1, 3))
                    
                else:
                    print(f"Failed to load {source['type']}: Status code {response.status_code}")
                    
            except Exception as e:
                print(f"Error scraping {source['type']}: {e}")
                continue
        
        # Return only the number of articles requested
        return all_articles[:num_articles]
    
    def is_similar_title(self, title1, title2):
        """Check if two titles are similar to avoid duplicates"""
        # Convert to lowercase and remove punctuation
        t1 = re.sub(r'[^\w\s]', '', title1.lower())
        t2 = re.sub(r'[^\w\s]', '', title2.lower())
        
        # If one title is contained in the other, consider them similar
        if t1 in t2 or t2 in t1:
            return True
            
        # Calculate word overlap
        words1 = set(t1.split())
        words2 = set(t2.split())
        
        # If they share more than 70% of words, consider them similar
        if len(words1) == 0 or len(words2) == 0:
            return False
            
        overlap = len(words1.intersection(words2)) / min(len(words1), len(words2))
        return overlap > 0.7

def main(company_name=None):
    scraper = NewsArticleScraper()
    
    # Get company name from user or use the provided one
    if company_name is None:
        company_name = input("Enter company name to search for: ")
    
    print(f"Searching for news about {company_name}...")
    articles = scraper.get_articles_for_company(company_name)
    
    # Output results as JSON
    output = {
        "company": company_name,
        "articles": articles,
        "total_articles": len(articles),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"Found {len(articles)} unique articles about {company_name}")
    
    # Create directory if it doesn't exist
    if not os.path.exists("news_articles"):
        os.makedirs("news_articles")
    
    # Save to file
    filename = f"news_articles/{company_name.replace(' ', '_').lower()}_news_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {filename}")
    
    # Print sample titles
    print("\nSample titles:")
    for i, article in enumerate(articles[:5], 1):
        print(f"{i}. {article['title']}")
    
    return output

if __name__ == "__main__":
    main()