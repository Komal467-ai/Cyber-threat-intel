"""
CVE (Vulnerability) Collector
Member 1: Data Collection & Preprocessing
"""

import requests
import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CVECollector:
    """Collects vulnerability data from National Vulnerability Database"""
    
    def __init__(self):
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    def fetch_recent_cves(self, days_back=7):
        """Fetch CVEs from last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        logger.info(f"Fetching CVEs from {start_str} to {end_str}")
        
        params = {
            'pubStartDate': start_str,
            'pubEndDate': end_str,
            'resultsPerPage': 20
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            cves = []
            for item in data.get('vulnerabilities', []):
                cve = item.get('cve', {})
                cves.append({
                    'id': cve.get('id'),
                    'description': cve.get('descriptions', [{}])[0].get('value', ''),
                    'published': cve.get('published'),
                    'severity': self._get_severity(cve)
                })
            
            logger.info(f"Fetched {len(cves)} CVEs")
            return cves
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def _get_severity(self, cve_data):
        """Extract severity score"""
        metrics = cve_data.get('metrics', {})
        if 'cvssMetricV31' in metrics:
            return metrics['cvssMetricV31'][0].get('cvssData', {}).get('baseScore', 'N/A')
        return 'N/A'
    
    def save_data(self, cves, filename='data/cve_raw.json'):
        """Save to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(cves),
                'cves': cves
            }, f, indent=2)
        logger.info(f"Saved to {filename}")


# Test
if __name__ == "__main__":
    collector = CVECollector()
    cves = collector.fetch_recent_cves(days_back=7)
    collector.save_data(cves)
    print(f"Collected {len(cves)} CVEs")