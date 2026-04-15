"""
Text Cleaner for Cybersecurity Data
Member 1: Data Preprocessing
"""

import re
import html


class CyberTextCleaner:
    """Cleans and normalizes security text"""
    
    def __init__(self):
        self.patterns = {
            'cve_id': r'CVE-\d{4}-\d{4,7}',
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'md5': r'\b[a-fA-F0-9]{32}\b',
            'sha256': r'\b[a-fA-F0-9]{64}\b',
            'url': r'https?://\S+'
        }
    
    def clean_html(self, text):
        """Remove HTML tags"""
        text = re.sub(r'<[^>]+>', ' ', text)
        return html.unescape(text)
    
    def extract_iocs(self, text):
        """Extract Indicators of Compromise"""
        iocs = {}
        for name, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                iocs[name] = matches
        return iocs
    
    def clean_text(self, text):
        """Full cleaning pipeline"""
        # Step 1: Remove HTML
        text = self.clean_html(text)
        
        # Step 2: Extract IoCs
        iocs = self.extract_iocs(text)
        
        # Step 3: Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text, iocs


# Test
if __name__ == "__main__":
    cleaner = CyberTextCleaner()
    test = "<p>Critical CVE-2024-1234 found in 192.168.1.1</p>"
    clean, iocs = cleaner.clean_text(test)
    print(f"Clean: {clean}")
    print(f"IoCs: {iocs}")