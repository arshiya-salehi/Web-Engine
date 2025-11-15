"""
Stemmer Module
Applies Porter stemming to tokens
"""

from nltk.stem import PorterStemmer
import nltk


class Stemmer:
    """Applies Porter stemming to tokens"""
    
    def __init__(self):
        # Download NLTK data if not already present
        try:
            self.stemmer = PorterStemmer()
        except LookupError:
            print("Downloading NLTK data...")
            nltk.download('punkt', quiet=True)
            self.stemmer = PorterStemmer()
    
    def stem(self, token):
        """
        Stem a single token
        
        Args:
            token: Input token string
            
        Returns:
            Stemmed token
        """
        return self.stemmer.stem(token)
    
    def stem_tokens(self, tokens):
        """
        Stem a list of tokens
        
        Args:
            tokens: List of token strings
            
        Returns:
            List of stemmed tokens
        """
        return [self.stem(token) for token in tokens]

