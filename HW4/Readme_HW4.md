
This assignment implements the **PageRank algorithm** to rank web pages based on their link structure.

PageRank determines the importance of a page by analyzing:

- The number of incoming links
- The quality of incoming links

The implementation processes a link graph file, iteratively computes PageRank scores, and outputs ranked pages.

## 1. Requirements

### Software

- Python 3.x

### Dependencies

No external packages are required.

The implementation uses only Python standard libraries.


## 2. Required Files

Place the following files in the same directory:
- `PageRank.py`
- `wt2g_inlinks.txt`

### Note

The original WT2g dataset is approximately **2GB**.

This implementation uses a **10.5 MB version of  WT2g** for testing and validation.
---

## 3. Algorithm

### PageRank Formula

    PR(A) = (1-d)/N + d × Σ(PR(B)/L(B))

Where:

d = damping factor
N = total number of pages
L(B) = number of outgoing links from page B
Parameters
Parameter	Value
Damping Factor	0.85
Random Jump Probability	0.15
Convergence Criterion	Perplexity change < 1 for 4 iterations
Perplexity Formula
    Perplexity = 2^(-Σ(PR(p) × log₂(PR(p))))


## 4. How to Run
Step 1: Open Terminal

Navigate to the project directory.

Step 2: Run the Program
python PageRank.py
Step 3: View Output

The program generates:

wt2g_rank.txt


## Files Used
PageRank.py		
wt2g_inlinks.txt
extract_stats.py - It automatically finds the numbers you need - the run time, sink nodes, number of round by running RageRank.py

Why Some Files Were Not Used like - Canonicalizer.y, Graph.py, HITS.py

The original homework distribution included additional files for graph construction and HITS computation.

These require:

Elasticsearch index hw3_crawl
Full WT2g document content
Outlink information

Since only the inlink graph file was available, only PageRank was implemented.