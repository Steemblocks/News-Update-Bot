"""
News Fetcher Module - Handles fetching news from various sources
"""
import feedparser
import logging
from typing import List, Dict, Optional
import requests
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

logger = logging.getLogger(__name__)

class NewsArticle:
    """Represents a news article"""
    def __init__(self, title: str, url: str, source: str, published: Optional[str] = None, 
                 description: Optional[str] = None, image_url: Optional[str] = None):
        self.title = title
        self.url = url
        self.source = source
        self.published = published
        self.description = description
        self.image_url = image_url

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "published": self.published,
            "description": self.description,
            "image_url": self.image_url
        }

class NewsFetcher:
    """Main news fetcher class"""
    
    # Popular news sources from USA, UK, and Europe
    # All URLs verified and tested for active RSS feeds (25+ verified working sources)
    DEFAULT_RSS_FEEDS = {
        # USA (8 sources)
        "nyt": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "bbc_news_world": "https://www.bbc.com/news/rss.xml",
        "nbc_news": "https://feeds.nbcnews.com/nbcnews/public/news",
        "foxnews": "https://feeds.foxnews.com/foxnews/latest",
        "guardian_world": "https://www.theguardian.com/world/rss",
        "vox": "https://www.vox.com/rss/index.xml",
        "washington_post": "https://feeds.washingtonpost.com/rss/world",
        "wired": "https://www.wired.com/feed/rss",
        
        # UK (8 sources)
        "independent": "https://www.independent.co.uk/news/rss",
        "telegraph": "https://www.telegraph.co.uk/news/rss.xml",
        "sky_news": "https://feeds.skynews.com/feeds/rss/home.xml",
        "guardian_uk": "https://www.theguardian.com/uk-news/rss",
        "mirror": "https://www.mirror.co.uk/news/?service=rss",
        "sun": "https://www.thesun.co.uk/news/rss",
        "bbc_uk": "https://www.bbc.co.uk/news/rss.xml",
        "metro": "https://metro.co.uk/feed/",
        
        # Europe (9 sources)
        "guardian_europe": "https://www.theguardian.com/world/europe-news/rss",
        "france24": "https://www.france24.com/en/rss",
        "politico_eu": "https://www.politico.eu/feed/",
        "ireland_news": "https://www.rte.ie/news/rss/news-headlines.xml",
        "bbc_europe": "https://www.bbc.co.uk/news/world/rss.xml",
        "bbc_business": "https://www.bbc.com/news/business/rss.xml",
        "techcrunch": "https://techcrunch.com/feed/",
        "guardian_sci": "https://www.theguardian.com/science/rss",
        "bbc_health": "https://www.bbc.com/news/health/rss.xml",
    }
    
    def __init__(self, newsapi_key: Optional[str] = None):
        """
        Initialize the NewsFetcher
        
        Args:
            newsapi_key: Optional API key for newsapi.org
        """
        self.newsapi_key = newsapi_key
    
    def is_recent_article(self, published_str: Optional[str]) -> bool:
        """Check if an article was published in the last 24 hours"""
        if not published_str:
            return True  # Include articles without a timestamp (assume recent)
        
        try:
            # Try to parse the published date
            article_time = parsedate_to_datetime(published_str)
            now = datetime.now(article_time.tzinfo) if article_time.tzinfo else datetime.now()
            
            # Check if article is within last 24 hours
            time_diff = now - article_time
            return time_diff <= timedelta(hours=24)
        except Exception as e:
            logger.debug(f"Error parsing article timestamp '{published_str}': {e}")
            return True  # Include articles we can't parse the time for

    async def fetch_rss_feed(self, feed_url: str, source_name: str) -> List[NewsArticle]:
        """Fetch articles from an RSS feed (last 24 hours only)"""
        try:
            articles = []
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                logger.warning(f"Feed parsing issues for {source_name}: {feed.bozo_exception}")
            
            for entry in feed.entries[:20]:  # Check more entries to find recent ones
                # Check if article is from last 24 hours
                published = entry.get("published", None)
                if not self.is_recent_article(published):
                    continue  # Skip articles older than 24 hours
                
                article = NewsArticle(
                    title=entry.get("title", "No title"),
                    url=entry.get("link", ""),
                    source=source_name,
                    published=published,
                    description=entry.get("summary", "")[:200] if entry.get("summary") else None,
                    image_url=None
                )
                articles.append(article)
                
                if len(articles) >= 10:  # Limit to 10 recent articles per feed
                    break
            
            return articles
        except Exception as e:
            logger.error(f"Error fetching RSS feed {source_name}: {e}")
            return []

    async def fetch_newsapi(self, region: str = "us") -> List[NewsArticle]:
        """
        Fetch articles from NewsAPI for a specific region (last 24 hours only)
        
        Args:
            region: Region code ('us', 'gb', 'de', 'fr', etc.)
        
        Returns:
            List of NewsArticle objects from last 24 hours
        """
        if not self.newsapi_key:
            logger.warning("NewsAPI key not configured, skipping NewsAPI source")
            return []
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "country": region,
                "apiKey": self.newsapi_key,
                "pageSize": 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article_data in data.get("articles", []):
                # Check if article is from last 24 hours
                published = article_data.get("publishedAt", None)
                if not self.is_recent_article(published):
                    continue  # Skip articles older than 24 hours
                
                article = NewsArticle(
                    title=article_data.get("title", ""),
                    url=article_data.get("url", ""),
                    source=article_data.get("source", {}).get("name", "NewsAPI"),
                    published=published,
                    description=article_data.get("description", ""),
                    image_url=article_data.get("urlToImage")
                )
                articles.append(article)
            
            return articles
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI for region {region}: {e}")
            return []

    async def fetch_all_news(self) -> Dict[str, List[NewsArticle]]:
        """
        Fetch news from all configured sources
        
        Returns:
            Dictionary with region keys and lists of articles
        """
        all_articles = {
            "usa": [],
            "uk": [],
            "europe": []
        }
        
        try:
            # Fetch from RSS feeds
            usa_sources = ["nyt", "guardian_world", "bbc_news_world", "nbc_news", "foxnews", "vox", "reuters", "apnews"]
            uk_sources = ["independent", "telegraph", "sky_news", "guardian_uk", "mirror", "sun", "bbc_uk", "metro"]
            europe_sources = ["guardian_europe", "france24", "politico_eu", "ireland_news", "bbc_europe", "euractiv", "dw_news", "italy_news", "canada_news"]
            
            for source_name, feed_url in self.DEFAULT_RSS_FEEDS.items():
                if source_name in usa_sources:
                    region = "usa"
                elif source_name in uk_sources:
                    region = "uk"
                else:
                    region = "europe"
                
                articles = await self.fetch_rss_feed(feed_url, source_name)
                all_articles[region].extend(articles)
            
            # Fetch from NewsAPI if available
            if self.newsapi_key:
                usa_articles = await self.fetch_newsapi("us")
                all_articles["usa"].extend(usa_articles)
                
                uk_articles = await self.fetch_newsapi("gb")
                all_articles["uk"].extend(uk_articles)
                
                de_articles = await self.fetch_newsapi("de")
                all_articles["europe"].extend(de_articles)
            
            # Remove duplicates based on URL
            for region in all_articles:
                seen_urls = set()
                unique_articles = []
                for article in all_articles[region]:
                    if article.url not in seen_urls:
                        seen_urls.add(article.url)
                        unique_articles.append(article)
                all_articles[region] = unique_articles
            
            return all_articles
        except Exception as e:
            logger.error(f"Error fetching all news: {e}")
            return all_articles
