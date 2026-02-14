"""
Training script for career recommendation models
"""
import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from data.career_dataset_generator import generate_dataset

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

def load_or_generate_dataset():
    """Load dataset or generate if it doesn't exist"""
    dataset_path = Path(__file__).parent.parent / 'data' / 'career_dataset.csv'
    
    if not dataset_path.exists():
        print("Dataset not found. Generating new dataset...")
        df = generate_dataset(n_records=1000)
    else:
        print(f"Loading dataset from {dataset_path}")
        df = pd.read_csv(dataset_path)
    
    return df

def prepare_features(df):
    """Prepare features for training"""
    # Select feature columns (exclude text columns)
    feature_cols = [col for col in df.columns if col not in [
        'technical_skills', 'soft_skills', 'interests', 'holland_code',
        'career', 'career_category', 'degree_level', 'academic_field'
    ]]
    
    X = df[feature_cols].fillna(0)
    y = df['career']
    
    return X, y, feature_cols

def train_random_forest(X_train, y_train, X_test, y_test):
    """Train Random Forest Classifier"""
    print("\n=== Training Random Forest Classifier ===")
    rf = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring='accuracy')
    print(f"Cross-validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return rf, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'cv_accuracy': cv_scores.mean(),
    }

def train_knn(X_train, y_train, X_test, y_test):
    """Train KNN Classifier"""
    print("\n=== Training KNN Classifier ===")
    knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
    knn.fit(X_train, y_train)
    
    # Evaluate
    y_pred = knn.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
    print(f"Cross-validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return knn, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'cv_accuracy': cv_scores.mean(),
    }

def train_neural_network(X_train, y_train, X_test, y_test, n_classes):
    """Train Neural Network"""
    print("\n=== Training Neural Network ===")
    
    # Normalize features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build model
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.Dense(n_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        X_train_scaled, y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )
    
    # Evaluate
    y_pred_proba = model.predict(X_test_scaled)
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    return model, scaler, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
    }

def main():
    """Main training function"""
    print("Starting Career Recommendation Model Training...")
    
    # Load or generate dataset
    df = load_or_generate_dataset()
    print(f"Dataset shape: {df.shape}")
    
    # Prepare features
    X, y, feature_cols = prepare_features(df)
    print(f"Features: {len(feature_cols)}")
    print(f"Classes: {len(y.unique())}")
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train models
    rf_model, rf_metrics = train_random_forest(X_train, y_train, X_test, y_test)
    knn_model, knn_metrics = train_knn(X_train, y_train, X_test, y_test)
    nn_model, scaler, nn_metrics = train_neural_network(X_train, y_train, X_test, y_test, len(label_encoder.classes_))
    
    # Save models
    models_dir = Path(__file__).parent.parent / 'ml_models'
    models_dir.mkdir(exist_ok=True)
    
    joblib.dump(rf_model, models_dir / 'random_forest_model.pkl')
    joblib.dump(knn_model, models_dir / 'knn_model.pkl')
    nn_model.save(models_dir / 'neural_network_model.h5')
    joblib.dump(scaler, models_dir / 'neural_network_scaler.pkl')
    joblib.dump(label_encoder, models_dir / 'label_encoder.pkl')
    joblib.dump(feature_cols, models_dir / 'feature_columns.pkl')
    
    print("\n=== Training Summary ===")
    print(f"Random Forest - Accuracy: {rf_metrics['accuracy']:.4f}")
    print(f"KNN - Accuracy: {knn_metrics['accuracy']:.4f}")
    print(f"Neural Network - Accuracy: {nn_metrics['accuracy']:.4f}")
    print(f"\nModels saved to {models_dir}")
    
    # Save training history to database (would be done via Django ORM in production)
    return {
        'random_forest': rf_metrics,
        'knn': knn_metrics,
        'neural_network': nn_metrics,
    }

if __name__ == '__main__':
    main()

