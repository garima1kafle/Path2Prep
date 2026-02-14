"""
NLP-based Scholarship Matching Engine
Implements TF-IDF + Cosine Similarity and BERT embeddings
"""
import os
import numpy as np
from pathlib import Path
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy
from .models import Scholarship
from profiles.models import Profile


class ScholarshipMatcher:
    """Scholarship matching engine using NLP"""
    
    def __init__(self):
        self.tfidf_vectorizer = None
        self.bert_model = None
        self.nlp = None
        self.use_bert = True
        self._load_models()
    
    def _load_models(self):
        """Load NLP models"""
        try:
            # Load spaCy model
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
                self.nlp = None
            
            # Load BERT model
            try:
                self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("BERT model loaded successfully")
            except Exception as e:
                print(f"Error loading BERT model: {e}. Using TF-IDF only.")
                self.use_bert = False
                self.bert_model = None
            
            # Initialize TF-IDF vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )
        except Exception as e:
            print(f"Error initializing NLP models: {e}")
    
    def _preprocess_text(self, text):
        """Preprocess text using spaCy"""
        if not text:
            return ""
        
        if self.nlp:
            doc = self.nlp(text.lower())
            # Remove stopwords, punctuation, and lemmatize
            tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
            return " ".join(tokens)
        else:
            # Fallback: simple preprocessing
            import re
            text = text.lower()
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            return text
    
    def _create_profile_text(self, profile):
        """Create text representation of user profile for matching"""
        text_parts = []
        
        if profile.degree_level:
            text_parts.append(f"degree level {profile.degree_level}")
        if profile.major:
            text_parts.append(f"major in {profile.major}")
        if profile.gpa:
            text_parts.append(f"GPA {profile.gpa}")
        if profile.country:
            text_parts.append(f"from {profile.country}")
        if profile.target_country:
            text_parts.append(f"targeting {profile.target_country}")
        
        # Test scores
        if profile.ielts_score:
            text_parts.append(f"IELTS score {profile.ielts_score}")
        if profile.toefl_score:
            text_parts.append(f"TOEFL score {profile.toefl_score}")
        if profile.gre_score:
            text_parts.append(f"GRE score {profile.gre_score}")
        if profile.gmat_score:
            text_parts.append(f"GMAT score {profile.gmat_score}")
        
        # Skills
        if profile.technical_skills:
            text_parts.append("skills: " + " ".join(profile.technical_skills))
        if profile.soft_skills:
            text_parts.append("skills: " + " ".join(profile.soft_skills))
        if profile.interests:
            text_parts.append("interested in: " + " ".join(profile.interests))
        
        # Financial need
        if profile.need_based_preference:
            text_parts.append("financial need based")
        if profile.income_range:
            text_parts.append(f"income range {profile.income_range}")
        
        return " ".join(text_parts)
    
    def _match_with_tfidf(self, profile_text, scholarship_texts):
        """Level 1: TF-IDF + Cosine Similarity matching"""
        if not self.tfidf_vectorizer:
            return None
        
        # Fit and transform
        all_texts = [profile_text] + scholarship_texts
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_texts)
        
        # Calculate cosine similarity
        profile_vector = tfidf_matrix[0:1]
        scholarship_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(profile_vector, scholarship_vectors)[0]
        return similarities
    
    def _match_with_bert(self, profile_text, scholarship_texts):
        """Level 2: BERT embeddings matching"""
        if not self.bert_model:
            return None
        
        # Generate embeddings
        profile_embedding = self.bert_model.encode([profile_text], convert_to_numpy=True)
        scholarship_embeddings = self.bert_model.encode(scholarship_texts, convert_to_numpy=True)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(profile_embedding, scholarship_embeddings)[0]
        return similarities
    
    def match_scholarships(self, user, top_k=5):
        """
        Match scholarships for a user
        Returns list of scholarships with relevance scores
        """
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            # Return all approved scholarships if profile doesn't exist
            scholarships = Scholarship.objects.filter(is_approved=True, is_active=True)[:top_k]
            return [
                {
                    'scholarship': scholarship,
                    'relevance_score': 0.5,
                    'method': 'default'
                }
                for scholarship in scholarships
            ]
        
        # Get all approved scholarships
        scholarships = Scholarship.objects.filter(is_approved=True, is_active=True)
        if not scholarships.exists():
            return []
        
        # Create profile text
        profile_text = self._create_profile_text(profile)
        profile_text_processed = self._preprocess_text(profile_text)
        
        # Create scholarship texts
        scholarship_texts = []
        for scholarship in scholarships:
            scholarship_text = f"{scholarship.title} {scholarship.description} {scholarship.eligibility}"
            scholarship_text_processed = self._preprocess_text(scholarship_text)
            scholarship_texts.append(scholarship_text_processed)
        
        # Level 1: TF-IDF matching
        tfidf_scores = self._match_with_tfidf(profile_text_processed, scholarship_texts)
        
        # Level 2: BERT matching (if available)
        if self.use_bert and self.bert_model:
            bert_scores = self._match_with_bert(profile_text, [f"{s.title} {s.description} {s.eligibility}" for s in scholarships])
            
            # Combine scores (weighted average)
            if tfidf_scores is not None:
                final_scores = 0.3 * tfidf_scores + 0.7 * bert_scores
                method = 'bert_tfidf_ensemble'
            else:
                final_scores = bert_scores
                method = 'bert'
        else:
            final_scores = tfidf_scores if tfidf_scores is not None else np.ones(len(scholarships)) * 0.5
            method = 'tfidf'
        
        # Get top K scholarships
        top_indices = np.argsort(final_scores)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'scholarship': scholarships[idx],
                'relevance_score': float(final_scores[idx]),
                'method': method
            })
        
        return results

