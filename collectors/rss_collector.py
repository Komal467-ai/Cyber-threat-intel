"""
RSS Feed Collector
Member 1: Data Collection & Preprocessing
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSCollector:
    """Collects cybersecurity articles from RSS feeds"""
    
    def __init__(self):
        self.feeds = {
            'bleeping_computer': 'https://www.bleepingcomputer.com/feed/',
            'the_hacker_news': 'https://thehackernews.com/feeds/posts/default',
            'dark_reading': 'https://www.darkreading.com/rss.xml'
        }
        self.collected_data = []
    
    def fetch_all_feeds(self):
        """Fetch all RSS feeds"""
        logger.info("Starting RSS collection...")
        
        for name, url in self.feeds.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:
                    article = {
                        'id': f"{name}_{hash(entry.title)}",
                        'source': name,
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'collected_at': datetime.now().isoformat()
                    }
                    self.collected_data.append(article)
                logger.info(f"✓ {name}: {len(feed.entries)} articles")
            except Exception as e:
                logger.error(f"✗ {name} failed: {e}")
        
        return self.collected_data
    
    def save_data(self, filename='data/rss_raw.json'):
        """Save to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(self.collected_data),
                'articles': self.collected_data
            }, f, indent=2)
        logger.info(f"Saved to {filename}")


# Test
if __name__ == "__main__":
    collector = RSSCollector()
    articles = collector.fetch_all_feeds()
    collector.save_data()
    print(f"Collected {len(articles)} articles")