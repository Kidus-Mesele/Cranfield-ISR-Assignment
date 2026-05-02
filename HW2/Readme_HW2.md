
This project implements a search engine from scratch using a custom inverted index.

Features:
- Tokenization (custom rules)
- Stopword removal (127 NLTK stopwords)
- Porter2 stemming
- Inverted index with term statistics
- Ranking models:
  - Okapi TF
  - BM25
  - Proximity Search

Two indexes are built:
- **Unstemmed index** (no stemming)
- **Stemmed index** (Porter2 stemming)


## Dataset

Cranfield Collection:
- 1,400 documents
- 225 queries
- Relevance judgments included

## Requirements


    pip install stemming
---

## How to Run
# 1. Build Indexes
python build_index.py

Output:

unstemmed_*.txt (4 files)
stemmed_*.txt (4 files)
# 2. Run Experiments

    python run_experiments.py

Generates:
results_OkapiTF_Unstemmed.txt
results_BM25_Unstemmed.txt
results_OkapiTF_Stemmed.txt
results_BM25_Stemmed.txt
results_Proximity.txt

# 3. Evaluate Results

    python evaluate.py

Or:

    trec_eval data/cranqrel.trec.txt results_BM25_Unstemmed.txt

## File Descriptions
File	Description
build_index.py	Builds indexes
index_reader.py	Reads index files
ranking.py	Ranking models
run_experiments.py	Runs experiments
evaluate.py	Computes MAP
tokenizer.py	Tokenization logic
