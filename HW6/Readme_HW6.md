This project applies machine learning to information retrieval by combining scores from multiple retrieval models as features to train a Linear Regression model. The trained model predicts document relevance and ranks documents accordingly.

## Dataset: Cranfield Collection (1,400 documents, 225 queries)

## Requirements
    pip install scikit-learn 


## How to Run
# Step 1: Add Your Input Files
Place your 6 HW1 result files into the results/ folder.

Place cranqrel.trec.txt into the data/ folder.

## Step 2: Run the Pipeline

    python feature_matrix.py
    python ml_ranker.py
    python evaluate.py
## What To Do With The Results
After running the code, you will get these files. Here is what to do with each:

1. results_ML_Linear.txt
What it is: ML-based ranking results in TREC format.

What to do: Evaluate this file using trec_eval to get MAP score.

bash

    trec_eval data/cranqrel.trec.txt results_ML_Linear.txt

Look for the line starting with map - this is your ML model's MAP score.

2. ml_coefficients.txt
What it is: Learned weights for each feature.

What to do: Open this file. It shows which retrieval models were most important (highest positive coefficients) and which were least important (negative or near-zero coefficients).

Use this to answer: Which model contributed most to the ML prediction

3. feature_matrix.csv
What it is: Feature vectors for all query-document pairs.

What to do: Open in Excel or any spreadsheet viewer. Each row has:

qid_doc: Query ID + Document ID

qid: Query number

docno: Document number

OkapiTF, TFIDF, BM25, Laplace, JelinekMercer, ES_Builtin: Scores from each model

label: Relevance (1 = relevant, 0 = not relevant)

Use this to verify that your feature matrix was created correctly.

4. Output from evaluate.py
What it is: MAP scores for all 7 models (6 individual + ML).

It helps you to Compare:
Which individual model performed best?
Did ML outperform the best individual model?
Which model performed worst?