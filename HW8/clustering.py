"""
HW8 - Topic Modeling and Clustering with 20 Newsgroups
"""

import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import time

print("="*60)
print("HW8 - TOPIC MODELING AND CLUSTERING")
print("20 Newsgroups Dataset")
print("="*60)

# Load parsed data
print("\n[1] Loading data...")
with open('newsgroups_data.pkl', 'rb') as f:
    data = pickle.load(f)

documents = data['documents']
labels = data['labels']
print(f"    Loaded {len(documents)} documents")
print(f"    Number of categories: {len(set(labels))}")

# Encode labels to numbers
print("\n[2] Encoding labels...")
label_encoder = LabelEncoder()
y_true = label_encoder.fit_transform(labels)
label_names = label_encoder.classes_
print(f"    Encoded {len(label_names)} unique labels")

# Create document-term matrix
print("\n[3] Creating document-term matrix...")
start = time.time()

vectorizer = CountVectorizer(
    max_features=5000,
    stop_words='english',
    max_df=0.95,
    min_df=2
)

dtm = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

print(f"    Shape: {dtm.shape[0]} docs x {dtm.shape[1]} terms")
print(f"    Time: {time.time() - start:.2f}s")

# LDA Topic Modeling
print("\n[4] Running LDA (Topic Modeling)...")
start = time.time()

n_topics = 20
lda = LatentDirichletAllocation(
    n_components=n_topics,
    random_state=42,
    max_iter=10,
    learning_method='online'
)

lda.fit(dtm)
print(f"    Extracted {n_topics} topics")
print(f"    Time: {time.time() - start:.2f}s")

# Print topics
print("\n[5] Top 10 words per topic:")
print("-" * 50)

for topic_idx, topic in enumerate(lda.components_):
    top_words_idx = topic.argsort()[-10:][::-1]
    top_words = [feature_names[i] for i in top_words_idx]
    print(f"Topic {topic_idx+1:2d}: {', '.join(top_words)}")

# Document-topic distribution
print("\n[6] Computing document-topic distribution...")
doc_topic = lda.transform(dtm)

# K-Means Clustering
print("\n[7] Running K-Means Clustering...")
start = time.time()

n_clusters = 20
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(doc_topic)

print(f"    Number of clusters: {n_clusters}")
print(f"    Time: {time.time() - start:.2f}s")

# Evaluate clustering
print("\n[8] Clustering Evaluation:")
ari = adjusted_rand_score(y_true, cluster_labels)
nmi = normalized_mutual_info_score(y_true, cluster_labels)

print(f"    Adjusted Rand Index (ARI): {ari:.4f}")
print(f"    Normalized Mutual Info (NMI): {nmi:.4f}")

print("\n    Interpretation:")
if ari > 0.3:
    print(f"    ✓ Good clustering quality (ARI > 0.3)")
    print(f"      The clusters align well with true newsgroup categories")
elif ari > 0.1:
    print(f"    ~ Moderate clustering quality (ARI > 0.1)")
else:
    print(f"    ✗ Poor clustering quality (ARI < 0.1)")

# Show cluster composition
print("\n[9] Cluster composition (first 8 clusters):")
for cluster_id in range(min(8, n_clusters)):
    cluster_docs = np.where(cluster_labels == cluster_id)[0]
    
    if len(cluster_docs) == 0:
        continue
    
    # Get dominant label in this cluster
    all_cluster_labels = [label_names[y_true[i]] for i in cluster_docs]
    dominant_label = Counter(all_cluster_labels).most_common(1)[0][0]
    purity = Counter(all_cluster_labels).most_common(1)[0][1] / len(cluster_docs)
    
    # Get sample of actual labels
    sample_labels = [label_names[y_true[i]] for i in cluster_docs[:5]]
    
    print(f"\n    Cluster {cluster_id}: {len(cluster_docs)} docs, {purity*100:.1f}% {dominant_label}")
    print(f"      Sample: {', '.join(sample_labels)}")

# Save results
print("\n[10] Saving results...")
with open('hw8_results.txt', 'w') as f:
    f.write("="*60 + "\n")
    f.write("HW8 - TOPIC MODELING AND CLUSTERING RESULTS\n")
    f.write("="*60 + "\n\n")
    
    f.write(f"Total documents: {len(documents)}\n")
    f.write(f"Number of newsgroups: {len(set(labels))}\n\n")
    
    f.write("LDA TOPICS (Top 10 words each):\n")
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-10:][::-1]
        top_words = [feature_names[i] for i in top_words_idx]
        f.write(f"Topic {topic_idx+1}: {', '.join(top_words)}\n")
    
    f.write(f"\nCLUSTERING EVALUATION:\n")
    f.write(f"Adjusted Rand Index (ARI): {ari:.4f}\n")
    f.write(f"Normalized Mutual Info (NMI): {nmi:.4f}\n")

print("\n    Saved to hw8_results.txt")

