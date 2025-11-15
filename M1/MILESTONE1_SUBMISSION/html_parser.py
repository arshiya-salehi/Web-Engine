"""
HTML Parser Module
Extracts text content from HTML, handling important tags (bold, headings, titles)
"""

from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import re
import warnings

# Suppress XML parsing warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class HTMLParser:
    """Parses HTML content and extracts text with importance markers"""
    
    def __init__(self):
        self.important_tags = ['strong', 'b', 'h1', 'h2', 'h3', 'title']
    
    def parse(self, html_content):
        """
        Parse HTML content and extract text with importance information
        
        Returns:
            dict with keys:
                - 'normal_text': list of normal text tokens
                - 'important_text': list of important text tokens (from bold, headings, titles)
        """
        # Use BeautifulSoup with html.parser which handles broken HTML well
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        normal_text = []
        important_text = []
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            important_text.append(title_tag.get_text())
        
        # Extract headings (h1, h2, h3)
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            important_text.append(heading.get_text())
        
        # Extract bold text (strong, b)
        for bold in soup.find_all(['strong', 'b']):
            important_text.append(bold.get_text())
        
        # Extract all other text (normal text)
        normal_text.append(soup.get_text())
        
        return {
            'normal_text': ' '.join(normal_text),
            'important_text': ' '.join(important_text)
        }

