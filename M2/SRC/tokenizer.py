"""
Tokenizer Module
Extracts alphanumeric sequences (tokens) from text
"""

import re


class Tokenizer:
    """Tokenizes text into alphanumeric sequences"""
    
    def __init__(self):
        # Pattern to match alphanumeric sequences
        self.token_pattern = re.compile(r'[a-zA-Z0-9]+')
    
    def tokenize(self, text):
        """
        Extract alphanumeric sequences from text
        
        Args:
            text: Input text string
            
        Returns:
            List of tokens (lowercased)
        """
        if not text:
            return []
        
        # Find all alphanumeric sequences and convert to lowercase
        tokens = self.token_pattern.findall(text.lower())
        return tokens

