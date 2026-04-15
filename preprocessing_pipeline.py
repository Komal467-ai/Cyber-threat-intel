"""
Main Data Preprocessing Pipeline
Member 1: Data Collection & Preprocessing
"""

import json
import logging
from datetime import datetime

from collectors.rss_collector import RSSCollector
from collectors.cve_collector import CVECollector
from utils.text_cleaner import CyberTextCleaner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPipeline:
    """End-to-end data collection and preprocessing"""
    
    def __init__(self):
        self.rss = RSSCollector()
        self.cve = CVECollector()
        self.cleaner = CyberTextCleaner()
    
    def run(self):
        """Execute full pipeline"""
        logger.info("="*50)
        logger.info("STARTING DATA PIPELINE")
        logger.info("="*50)
        
        # Step 1: Collect RSS
        logger.info("[1/3] Collecting RSS feeds...")
        rss_data = self.rss.fetch_all_feeds()
        self.rss.save_data('data/rss_raw.json')
        
        # Step 2: Collect CVE
        logger.info("[2/3] Collecting CVE data...")
        cve_data = self.cve.fetch_recent_cves(days_back=7)
        self.cve.save_data(cve_data, 'data/cve_raw.json')
        
        # Step 3: Clean RSS data
        logger.info("[3/3] Cleaning data...")
        cleaned = []
        for article in rss_data:
            text, iocs = self.cleaner.clean_text(
                article.get('title', '') + ' ' + article.get('summary', '')
            )
            cleaned.append({
                'id': article['id'],
                'source': article['source'],
                'cleaned_text': text,
                'iocs': iocs,
                'link': article['link']
            })
        
        # Save cleaned data
        with open('data/cleaned_data.json', 'w') as f:
            json.dump({
                'processed_at': datetime.now().isoformat(),
                'articles': cleaned
            }, f, indent=2)
        
        logger.info(f"✓ Pipeline complete: {len(cleaned)} articles processed")
        return cleaned


# Run when executed
if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run()