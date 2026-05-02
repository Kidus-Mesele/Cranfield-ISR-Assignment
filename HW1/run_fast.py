from elasticsearch import Elasticsearch
import math
import xml.etree.ElementTree as ET
import re
from collections import defaultdict
import time

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
print("✓ Connected to Elasticsearch")

# Get all documents and pre-compute lengths
print("\nLoading all documents...")
all_docs_resp = es.search(index="cranfield", body={"size": 10000, "_source": ["docno", "length"]})
all_docs = []
doc_lengths = {}
for hit in all_docs_resp["hits"]["hits"]:
    doc_id = hit["_id"]
    all_docs.append(doc_id)
    doc_lengths[doc_id] = hit["_source"]["length"]
print(f"✓ Loaded {len(all_docs)} documents")

# Get N and avgdl
N = len(all_docs)
avgdl = sum(doc_lengths.values()) / N
print(f"✓ N={N}, avgdl={avgdl:.2f}")

# Load all queries
tree = ET.parse("cran.qry.xml")
root = tree.getroot()
queries = []
for topic in root.findall(".//top"):
    num = topic.findtext("num").strip()
    title = topic.findtext("title").strip()
    title = re.sub(r'\s+', ' ', title.lower()).strip()
    title = re.sub(r'[^\w\s]', '', title)
    queries.append({"id": num, "terms": title.split()})
print(f"✓ Loaded {len(queries)} queries")

# Pre-compute term stats
print("\nPre-computing term statistics...")
term_df = {}
term_tf = defaultdict(dict)
total_terms = 0

for doc_id in all_docs:
    resp = es.termvectors(index="cranfield", id=doc_id, fields=["text"])
    if "term_vectors" in resp and "text" in resp["term_vectors"]:
        terms_dict = resp["term_vectors"]["text"]["terms"]
        doc_len = doc_lengths[doc_id]
        total_terms += doc_len
        for term, info in terms_dict.items():
            tf = info["term_freq"]
            term_tf[term][doc_id] = tf

# Compute DF from TF dict
for term in term_tf:
    term_df[term] = len(term_tf[term])

V = total_terms
print(f"✓ Vocabulary size: {V}")

# Scoring functions (optimized - no ES calls)
def score_bm25(query_terms, doc_id, k1=1.2, b=0.75):
    score = 0.0
    doc_len = doc_lengths[doc_id]
    for term in query_terms:
        if term not in term_tf:
            continue
        tf = term_tf[term].get(doc_id, 0)
        if tf == 0:
            continue
        df = term_df[term]
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
        tf_part = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl)))
        score += idf * tf_part
    return score

def score_laplace(query_terms, doc_id):
    score = 0.0
    doc_len = doc_lengths[doc_id]
    for term in query_terms:
        if term not in term_tf:
            tf = 0
        else:
            tf = term_tf[term].get(doc_id, 0)
        prob = (tf + 1) / (doc_len + V)
        score += math.log(prob)
    return score

def score_jelinek(query_terms, doc_id, lam=0.7):
    score = 0.0
    doc_len = doc_lengths[doc_id]
    for term in query_terms:
        if term not in term_tf:
            tf = 0
        else:
            tf = term_tf[term].get(doc_id, 0)
        p_doc = tf / doc_len if doc_len > 0 else 0
        p_collection = 1.0 / V
        prob = lam * p_doc + (1 - lam) * p_collection
        if prob > 0:
            score += math.log(prob)
    return score

# Run BM25
print("\n" + "=" * 50)
print("Running BM25...")
print("=" * 50)
with open("results_BM25.txt", "w") as out:
    for q in queries:
        qid = q["id"]
        terms = q["terms"]
        scores = []
        for doc_id in all_docs:
            score = score_bm25(terms, doc_id)
            if score > 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        for rank, (doc_id, score) in enumerate(scores[:100], 1):
            out.write(f"{qid} Q0 {doc_id} {rank} {score:.6f} BM25\n")
print("✓ BM25 done")

# Run Laplace
print("\n" + "=" * 50)
print("Running Laplace LM...")
print("=" * 50)
with open("results_Laplace.txt", "w") as out:
    for q in queries:
        qid = q["id"]
        terms = q["terms"]
        scores = []
        for doc_id in all_docs:
            score = score_laplace(terms, doc_id)
            if score != 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        for rank, (doc_id, score) in enumerate(scores[:100], 1):
            out.write(f"{qid} Q0 {doc_id} {rank} {score:.6f} Laplace\n")
print("✓ Laplace done")

# Run Jelinek-Mercer
print("\n" + "=" * 50)
print("Running Jelinek-Mercer LM...")
print("=" * 50)
with open("results_JelinekMercer.txt", "w") as out:
    for q in queries:
        qid = q["id"]
        terms = q["terms"]
        scores = []
        for doc_id in all_docs:
            score = score_jelinek(terms, doc_id)
            if score != 0:
                scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        for rank, (doc_id, score) in enumerate(scores[:100], 1):
            out.write(f"{qid} Q0 {doc_id} {rank} {score:.6f} JelinekMercer\n")
print("✓ Jelinek-Mercer done")

print("\n" + "=" * 50)
print("ALL DONE! 3 new result files created:")
print("  - results_BM25.txt")
print("  - results_Laplace.txt")
print("  - results_JelinekMercer.txt")
print("=" * 50)
