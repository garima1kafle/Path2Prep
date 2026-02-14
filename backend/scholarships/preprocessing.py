"""
Text preprocessing utilities for scholarship matching
"""
import re
import spacy


def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def tokenize_text(text, nlp=None):
    """Tokenize text using spaCy if available"""
    if not text:
        return []
    
    if nlp:
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
        return tokens
    else:
        # Simple tokenization fallback
        return text.split()


def remove_stopwords(text, nlp=None):
    """Remove stopwords from text"""
    if not text:
        return ""
    
    if nlp:
        doc = nlp(text)
        tokens = [token.text for token in doc if not token.is_stop]
        return " ".join(tokens)
    else:
        return text

