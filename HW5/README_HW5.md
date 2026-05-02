
This project implements a TREC (Text REtrieval Conference) evaluation pipeline to evaluate the performance of an Elasticsearch-based search engine.

The system:

- Runs 3 search queries against an Elasticsearch index
- Generates ranked retrieval results
- Creates relevance judgments (qrels)
- Calculates standard Information Retrieval (IR) evaluation metrics
- Produces Precision-Recall data for visualization


## 1. Requirements

### Software

- Python 3.x
- Elasticsearch 7.x (running locally on port 9200)
- Internet connection (for package installation)

### Python Packages

Install required packages using:

```bash
pip install elasticsearch elasticsearch-dsl
```

---



## 3. Queries Used

| Query ID | Query Text |
|----------|------------|
| 151801 | Causes of world war 2 |
| 151802 | Battles won by USA in World War 2 |
| 151803 | Battle of Stalingrad |

---

## 4. How to Run

### Step 1: Start Elasticsearch

```bash
curl http://localhost:9200
```

### Step 2: Update Configuration

```python
INDEX_NAME = "cranfield"
FIELD_NAME = "text"
```

### Step 3: Generate Ranked Results

```bash
python Trec_Prep.py
```

### Step 4: Calculate Evaluation Metrics

```bash
python Trec_Eval_Improved.py
```

### Step 5: Create Precision-Recall Data

```bash
python create_pr_csv.py
```

### Step 6: Create Precision-Recall Graph

1. Open `pr_data.csv` in Excel
2. Select Precision and Recall columns
3. Insert Scatter Plot
4. Save as `Precision-Recall.xlsx`

---

## 6. Relevance Judgment Method

| Rank Position | Relevance |
|--------------|-----------|
| 1 | 0 (Not Relevant) |
| 2–50 | 1 (Relevant) |
| 51+ | 0 (Not Relevant) |

Total relevant documents per query: **49**

---

## 7. Evaluation Metrics

- MAP
- Precision@k
- Recall@k
- F1-score@k
- nDCG
- R-Precision

---

## 8. File Descriptions

| File | Description |
|------|-------------|
| `Trec_Prep.py` | Runs queries against Elasticsearch |
| `Trec_Eval_Improved.py` | Calculates evaluation metrics |
| `create_pr_csv.py` | Creates Precision-Recall data |
| `qrels.txt` | Relevance judgments |
| `rankList.txt` | Ranked retrieval results |
| `details.txt` | Precision/Recall details |
| `pr_data.csv` | Precision-Recall graph data |
| `Precision-Recall.xlsx` | Precision-Recall graph |
| `Graphs.xlsx` | Graph template |
| `README.md` | Setup and usage instructions |
| `Report.pdf` | Documentation and analysis |

---


