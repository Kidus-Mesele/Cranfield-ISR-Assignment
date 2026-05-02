## Overview
This project implements a machine learning classifier for automatically distinguishing between:

- **Spam** (unwanted or junk email)
- **Ham** (legitimate email)

The classifier uses:

- **TF-IDF vectorization** for text feature extraction  
- **Logistic Regression** for binary classification  
- **5-fold cross-validation** for model evaluation  

This project demonstrates how machine learning can be applied to email filtering tasks.


## 2. Dataset

This project uses a **pre-processed version** of the TREC 2007 Spam Track dataset.
You can download it from: https://www.kaggle.com/datasets/imdeepmind/preprocessed-trec-2007-public-corpus-dataset

The original raw `.eml` files were not used directly.


## 3. Requirements

### Software

- Python 3.x

### Required Packages

```bash
pip install pandas scikit-learn joblib
```

---

## 4. Required Files

- processed_data.csv  
- train_classifier.py  
- report.py  

---

## 5. How to Run

### Step 1: Install Dependencies

```bash
pip install pandas scikit-learn joblib
```

### Step 2: Train the Classifier

```bash
python train_classifier.py
```

### Step 3: Generate Report

```bash
python report.py
```

---

## 6. Model Parameters

- Max Features: 5,000  
- Min Document Frequency: 2  
- Max Document Frequency: 95%  
- Stop Words: English  
- Test Split: 80/20  
- Cross Validation: 5-fold  

---

## 7. Output Files

- spam_classifier.pkl  
- tfidf_vectorizer.pkl  
- evaluation reports  
---
Output Files Created
File Description 
What to do with it?
spam_classifier.pkl	Saved trained model	Keep for future predictions
tfidf_vectorizer.pkl	Saved vectorizer	Keep for transforming new emails

Results Printed to Console
The script will output:


Accuracy: 99.66%	Model correctness on test data	Include in report
Confusion Matrix	Shows correct/incorrect predictions	Include in report
Classification Report	Precision, Recall, F1 per class	Include in report
Top Spam/Ham words	Most important features	Include in report
Cross-validation scores	Model robustness check	Include in report

How to Test with New Emails
After training, you can classify new emails using the saved model:

python
import joblib

# Load model and vectorizer
clf = joblib.load('spam_classifier.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# New email text
new_email = "Subject: Buy cheap pills now! Click here..."

# Transform and predict
X_new = vectorizer.transform([new_email])
prediction = clf.predict(X_new)[0]

print("SPAM" if prediction == 1 else "HAM")



