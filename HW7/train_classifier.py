"""
HW7 - Spam/Ham Email Classifier
Trains Logistic Regression on email text
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import time

print("="*60)
print("HW7 - SPAM/HAM EMAIL CLASSIFIER")
print("="*60)

# Step 1: Load data
print("\n[1] Loading data...")
df = pd.read_csv("processed_data.csv")
print(f"    Loaded {len(df)} emails")
print(f"    Spam: {(df['label']==1).sum()} emails")
print(f"    Ham:  {(df['label']==0).sum()} emails")

# Step 2: Combine text fields
print("\n[2] Combining text fields...")
# Fill missing values with empty string
df['subject'] = df['subject'].fillna('')
df['email_to'] = df['email_to'].fillna('')
df['email_from'] = df['email_from'].fillna('')
df['message'] = df['message'].fillna('')

# Combine all text
df['full_text'] = df['subject'] + ' ' + df['email_to'] + ' ' + df['email_from'] + ' ' + df['message']
print(f"    Example: {df['full_text'].iloc[0][:150]}...")

# Step 3: Convert text to TF-IDF features
print("\n[3] Converting text to TF-IDF features...")
print("    This may take 1-2 minutes for 75,000 emails...")
start_time = time.time()

vectorizer = TfidfVectorizer(
    max_features=5000,        # Use top 5000 words
    stop_words='english',      # Remove common words
    lowercase=True,
    min_df=2,                  # Ignore words that appear in less than 2 emails
    max_df=0.95               # Ignore words that appear in >95% of emails
)

X = vectorizer.fit_transform(df['full_text'])
y = df['label'].values

print(f"    Time taken: {time.time() - start_time:.1f} seconds")
print(f"    Feature matrix shape: {X.shape}")

# Step 4: Split into train and test
print("\n[4] Splitting into train (80%) and test (20%)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"    Training: {len(y_train)} emails")
print(f"    Testing: {len(y_test)} emails")

# Step 5: Train classifier
print("\n[5] Training Logistic Regression classifier...")
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train, y_train)

# Step 6: Evaluate
print("\n[6] Evaluating on test set...")
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*60}")
print(f"ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*60}")

print("\n[7] Detailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Ham (0)', 'Spam (1)']))

print("\n[8] Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"                    Predicted")
print(f"                    Ham    Spam")
print(f"Actual  Ham        {cm[0,0]:6d}  {cm[0,1]:6d}")
print(f"        Spam       {cm[1,0]:6d}  {cm[1,1]:6d}")

# Step 9: Cross-validation
print("\n[9] 5-Fold Cross Validation...")
cv_scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
print(f"    CV Scores: {cv_scores}")
print(f"    Mean CV Accuracy: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")

# Step 10: Top features
print("\n[10] Top 20 Most Important Features (Words):")
feature_names = vectorizer.get_feature_names_out()
coefs = clf.coef_[0]

# Get top features for spam (positive coefficients)
top_spam_idx = coefs.argsort()[-20:][::-1]
top_ham_idx = coefs.argsort()[:20]

print("\n    Top Spam Indicators (words that predict SPAM):")
for idx in top_spam_idx:
    print(f"        {feature_names[idx]}: {coefs[idx]:.4f}")

print("\n    Top Ham Indicators (words that predict HAM):")
for idx in top_ham_idx:
    print(f"        {feature_names[idx]}: {coefs[idx]:.4f}")

print("\n" + "="*60)
print("CLASSIFIER TRAINING COMPLETE!")
print("="*60)

# Save the model for later use
import joblib
joblib.dump(clf, 'spam_classifier.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
print("\nModel saved to 'spam_classifier.pkl' and 'tfidf_vectorizer.pkl'")