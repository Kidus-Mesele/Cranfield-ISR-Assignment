
## 1. Overview
This assignment applies unsupervised learning techniques for text analysis:

- **Topic Modeling** using Latent Dirichlet Allocation (LDA)
- **Document Clustering** using K-Means on LDA topic distributions
- **Evaluation** using:
  - Adjusted Rand Index (ARI)
  - Normalized Mutual Information (NMI)

## 2. Dataset

The **20 Newsgroups dataset** was used for this assignment.

**Note:** The original AP89 dataset was unavailable/corrupted, so the 20 Newsgroups dataset was used instead.
---

## 3. Requirements

### Software
- Python 3.x

### Python Libraries

Install required packages:

```bash
pip install scikit-learn numpy
```
## 4. How to Run
Step 1: Parse the Dataset

    python parse_20newsgroups.py

This will:

Read raw dataset files
Extract documents and labels
Save processed data to newsgroups_data.pkl

Step 2: Run Clustering

    python clustering.py

This will:
Load processed dataset
Create document-term matrix
Apply LDA topic modeling
Run K-Means clustering
Compute ARI and NMI scores
Save results to hw8_results.txt

7. Parameters Used
Stage               Parameter         Value
Vectorizer	        max_features	    5,000
Vectorizer	        stop_words	      english
LDA	                n_components	    20
LDA	                max_iter	        10
K-Means	            n_clusters	      20
K-Means	            n_init	          10

8. Results Interpretation
Topics
Each topic contains top words representing a theme (e.g., politics, religion, computers, sports).
Example:
Topic 5: jesus, christ, lord, father, son, paul  
Topic 8: gun, police, weapons, arms, gas  
Topic 10: windows, drive, dos, problem

Evaluation Metrics

ARI (Adjusted Rand Index)
Measures clustering similarity to ground truth
0 ≈ random clustering
1 ≈ perfect clustering

NMI (Normalized Mutual Information)
Measures agreement between clusters and true labels
0 ≈ no relationship
1 ≈ perfect match

Example:
ARI: 0.1138  
NMI: 0.2587

Cluster Purity
Example:
Cluster 7: 74.7% talk.politics.mideast
