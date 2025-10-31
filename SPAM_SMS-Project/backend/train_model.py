# backend/train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib
import os

def train_and_save_model():
    # Load your dataset
    print("Loading dataset...")
    df = pd.read_csv('SPAM_SMS.csv')  # Make sure this file is in your backend directory
    
    # Preprocessing steps from your notebook
    print("Preprocessing data...")
    # Add any preprocessing steps you did in the notebook
    # For example:
    # df['text'] = df['text'].str.lower()
    
    # Split into features and target
    X = df['text']
    y = df['label']
    
    # Create TF-IDF vectorizer
    print("Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    # Transform the text data
    X_tfidf = vectorizer.fit_transform(X)
    
    # Train the model
    print("Training model...")
    model = MultinomialNB()
    model.fit(X_tfidf, y)
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model and vectorizer with names that app.py looks for
    model_path = 'spam_detector_model.pkl'
    vectorizer_path = 'tfidf_vectorizer.pkl'
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    # Also save with alternative names for backward compatibility
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    print(f"\nModel saved to {model_path} and model.pkl")
    print(f"Vectorizer saved to {vectorizer_path} and vectorizer.pkl")
    
    # Print model performance
    y_pred = model.predict(X_tfidf)
    print("\nTraining performance:")
    print(classification_report(y, y_pred, target_names=['ham', 'spam']))

if __name__ == "__main__":
    train_and_save_model()