"""
ML Engine for Career Recommendations
Implements Random Forest, KNN, and Neural Network models with ensemble voting
"""
import os
from pathlib import Path
from django.conf import settings
from careers.models import Career
from profiles.models import Profile

# Optional ML imports
try:
    import joblib
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    import tensorflow as tf
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    joblib = None
    np = None
    pd = None
    StandardScaler = None
    tf = None


class CareerRecommendationEngine:
    """Career recommendation engine using ML models"""
    
    def __init__(self):
        self.models_dir = Path(settings.BASE_DIR) / 'ml_models'
        self.models_loaded = False
        self.rf_model = None
        self.knn_model = None
        self.nn_model = None
        self.nn_scaler = None
        self.label_encoder = None
        self.feature_cols = None
        self._load_models()
    
    def _load_models(self):
        """Load trained ML models"""
        if not ML_AVAILABLE:
            print("ML libraries not available. Using default recommendations.")
            self.models_loaded = False
            return
        
        try:
            # Load models
            rf_path = self.models_dir / 'random_forest_model.pkl'
            knn_path = self.models_dir / 'knn_model.pkl'
            nn_path = self.models_dir / 'neural_network_model.h5'
            scaler_path = self.models_dir / 'neural_network_scaler.pkl'
            encoder_path = self.models_dir / 'label_encoder.pkl'
            features_path = self.models_dir / 'feature_columns.pkl'
            
            if all(p.exists() for p in [rf_path, knn_path, nn_path, scaler_path, encoder_path, features_path]):
                self.rf_model = joblib.load(rf_path)
                self.knn_model = joblib.load(knn_path)
                self.nn_model = tf.keras.models.load_model(nn_path)
                self.nn_scaler = joblib.load(scaler_path)
                self.label_encoder = joblib.load(encoder_path)
                self.feature_cols = joblib.load(features_path)
                self.models_loaded = True
                print("ML models loaded successfully")
            else:
                print("ML models not found. Using default recommendations.")
                self.models_loaded = False
        except Exception as e:
            print(f"Error loading models: {e}")
            self.models_loaded = False
    
    def _extract_features_from_profile(self, profile):
        """Extract features from user profile"""
        features = {}
        
        # GPA
        features['gpa'] = float(profile.gpa) if profile.gpa else 3.0
        
        # Degree level encoding
        degree_mapping = {'Bachelor\'s': 1, 'Master\'s': 2, 'PhD': 3}
        features['degree_level_encoded'] = degree_mapping.get(profile.degree_level, 1)
        
        # Technical skills (binary features)
        tech_skills = profile.technical_skills or []
        for skill in ['Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 
                     'Data Analysis', 'Web Development', 'Mobile Development', 
                     'Cloud Computing', 'Statistics']:
            features[f'has_{skill.lower().replace(" ", "_")}'] = 1 if skill in tech_skills else 0
        
        # Soft skills (binary features)
        soft_skills = profile.soft_skills or []
        for skill in ['Communication', 'Leadership', 'Problem Solving', 'Teamwork', 
                     'Critical Thinking', 'Creativity', 'Time Management']:
            features[f'has_{skill.lower().replace(" ", "_")}'] = 1 if skill in soft_skills else 0
        
        # Interests (binary features)
        interests = profile.interests or []
        for interest in ['Technology', 'Research', 'Business', 'Arts', 'Healthcare', 'Education']:
            features[f'interest_{interest.lower().replace(" ", "_")}'] = 1 if interest in interests else 0
        
        # Holland Code
        holland_code = profile.holland_code or ''
        for code in ['R', 'I', 'A', 'S', 'E', 'C']:
            features[f'holland_{code}'] = holland_code.count(code)
        
        return features
    
    def _create_feature_vector(self, features):
        """Create feature vector matching training data format"""
        if not ML_AVAILABLE or not self.feature_cols:
            return None
        
        # Create DataFrame with all feature columns
        feature_dict = {col: 0 for col in self.feature_cols}
        
        # Update with actual values
        for key, value in features.items():
            if key in feature_dict:
                feature_dict[key] = value
        
        # Convert to DataFrame and ensure correct order
        df = pd.DataFrame([feature_dict])
        return df[self.feature_cols].fillna(0).values[0]
    
    def _predict_with_ensemble(self, feature_vector):
        """Get predictions from all models and ensemble them"""
        predictions = {}
        probabilities = {}
        
        # Random Forest
        rf_proba = self.rf_model.predict_proba([feature_vector])[0]
        rf_pred = self.rf_model.predict([feature_vector])[0]
        predictions['random_forest'] = rf_pred
        probabilities['random_forest'] = rf_proba
        
        # KNN
        knn_proba = self.knn_model.predict_proba([feature_vector])[0]
        knn_pred = self.knn_model.predict([feature_vector])[0]
        predictions['knn'] = knn_pred
        probabilities['knn'] = knn_proba
        
        # Neural Network
        feature_scaled = self.nn_scaler.transform([feature_vector])
        nn_proba = self.nn_model.predict(feature_scaled, verbose=0)[0]
        nn_pred = np.argmax(nn_proba)
        predictions['neural_network'] = nn_pred
        probabilities['neural_network'] = nn_proba
        
        # Ensemble: Average probabilities
        ensemble_proba = (
            probabilities['random_forest'] * 0.4 +
            probabilities['knn'] * 0.3 +
            probabilities['neural_network'] * 0.3
        )
        
        return ensemble_proba, predictions
    
    def get_recommendations(self, user, top_k=3):
        """
        Get top K career recommendations for a user
        Returns list of dicts with 'career', 'confidence', 'model' keys
        """
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            # Return default recommendations if profile doesn't exist
            careers = Career.objects.all()[:top_k]
            return [
                {
                    'career': career,
                    'confidence': 0.5,
                    'model': 'default'
                }
                for career in careers
            ]
        
        # If models not loaded, return default recommendations
        if not self.models_loaded:
            careers = Career.objects.all()[:top_k]
            return [
                {
                    'career': career,
                    'confidence': 0.6,
                    'model': 'default'
                }
                for career in careers
            ]
        
        # Extract features from profile
        features = self._extract_features_from_profile(profile)
        feature_vector = self._create_feature_vector(features)
        
        # Get ensemble predictions
        ensemble_proba, individual_predictions = self._predict_with_ensemble(feature_vector)
        
        # Get top K predictions
        top_indices = np.argsort(ensemble_proba)[-top_k:][::-1]
        top_careers_encoded = [self.label_encoder.classes_[idx] for idx in top_indices]
        top_confidences = [float(ensemble_proba[idx]) for idx in top_indices]
        
        # Get Career objects
        recommendations = []
        for career_name, confidence in zip(top_careers_encoded, top_confidences):
            try:
                career = Career.objects.get(name=career_name)
            except Career.DoesNotExist:
                # Create career if it doesn't exist
                career = Career.objects.create(
                    name=career_name,
                    description=f"Career recommendation: {career_name}",
                    category="Recommended"
                )
            
            recommendations.append({
                'career': career,
                'confidence': confidence,
                'model': 'ensemble'
            })
        
        return recommendations
