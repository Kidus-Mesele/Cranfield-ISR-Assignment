"""
Creates Precision-Recall CSV for Excel graphing
"""

from collections import defaultdict

def load_qrels(qrel_file):
    """Load relevance judgments"""
    qrels = defaultdict(set)
    with open(qrel_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4:
                qid = parts[0]
                doc_id = parts[2]
                rel = int(parts[3])
                if rel > 0:
                    qrels[qid].add(doc_id)
    return qrels

def load_results(results_file):
    """Load ranked results"""
    results = defaultdict(list)
    with open(results_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 6:
                qid = parts[0]
                doc_id = parts[2]
                results[qid].append(doc_id)
    return results

def compute_pr_points(qrels_set, results_list):
    """
    Compute precision and recall at each rank
    Returns list of (precision, recall, rank) tuples
    """
    points = []
    rel_ret = 0
    total_rel = len(qrels_set)
    
    if total_rel == 0:
        return points
    
    for rank, doc_id in enumerate(results_list[:100], start=1):
        if doc_id in qrels_set:
            rel_ret += 1
        
        precision = rel_ret / rank
        recall = rel_ret / total_rel
        
        points.append((rank, precision, recall))
    
    return points

def main():
    print("Creating Precision-Recall CSV...")
    print("-" * 40)
    
    # Load files
    qrels = load_qrels("qrels.txt")
    results = load_results("rankList.txt")
    
    print(f"Loaded {len(qrels)} queries from qrels.txt")
    print(f"Loaded {len(results)} queries from rankList.txt")
    
    # Write CSV
    with open("pr_data.csv", "w") as f:
        f.write("QueryID,Rank,Precision,Recall\n")
        
        for qid in sorted(results.keys()):
            if qid not in qrels:
                print(f"Warning: {qid} not in qrels.txt - skipping")
                continue
            
            points = compute_pr_points(qrels[qid], results[qid])
            
            for rank, precision, recall in points:
                f.write(f"{qid},{rank},{precision:.6f},{recall:.6f}\n")
            
            print(f"Query {qid}: {len(points)} data points")
    
    print("-" * 40)
    print("Done! Created pr_data.csv")
    print("\nNext steps:")
    print("1. Open pr_data.csv in Excel")
    print("2. Insert Scatter Plot (smooth lines)")
    print("3. X-axis = Recall, Y-axis = Precision")
    print("4. Save as Precision-Recall.xlsx")

if __name__ == "__main__":
    main()