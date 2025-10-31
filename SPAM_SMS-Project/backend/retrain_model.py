import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# File paths
dataset_path = os.path.join('SPAM_SMS.csv')
model_path = 'spam_detector_model.pkl'
vectorizer_path = 'tfidf_vectorizer.pkl'

print("Loading dataset...")
df = pd.read_csv(dataset_path, encoding='latin-1')

# Preprocess data
df = df[['v1', 'v2']]  # Keep only label and text columns
df.columns = ['label', 'text']
df['label'] = df['label'].map({'ham': 0, 'spam': 1})  # Convert labels to binary

# Split data
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training vectorizer...")
# Create and fit the vectorizer
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)

print("Training model...")
# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Save the model and vectorizer
print("Saving model and vectorizer...")
joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

# Evaluate the model
print("\nModel Evaluation:")
X_test_tfidf = vectorizer.transform(X_test)
y_pred = model.predict(X_test_tfidf)
print(classification_report(y_test, y_pred, target_names=['ham', 'spam']))

print(f"\nModel saved to {model_path}")
print(f"Vectorizer saved to {vectorizer_path}")
