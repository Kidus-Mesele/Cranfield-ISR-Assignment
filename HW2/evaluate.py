import sys
from collections import defaultdict

def load_qrels(qrel_file="data/cranqrel.trec.txt"):
    qrels = defaultdict(dict)
    with open(qrel_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                qid, _, docid, rel = parts
                qrels[qid][docid] = int(rel)
    return qrels

def load_results(results_file):
    results = defaultdict(list)
    with open(results_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 6:
                qid = parts[0]
                docid = parts[2]
                results[qid].append(docid)
    return results

def compute_ap(qrels_dict, results_list):
    num_rel = sum(1 for rel in qrels_dict.values() if rel > 0)
    if num_rel == 0:
        return 0.0
    
    rel_ret = 0
    sum_prec = 0.0
    
    for i, docid in enumerate(results_list, 1):
        if qrels_dict.get(docid, 0) > 0:
            rel_ret += 1
            sum_prec += rel_ret / i
    
    return sum_prec / num_rel

def evaluate_single(results_file):
    print(f"\n{results_file}:")
    print("-" * 50)
    
    qrels = load_qrels()
    results = load_results(results_file)
    
    ap_scores = []
    q_count = 0
    
    for qid in sorted(results.keys(), key=lambda x: int(x)):
        if qid in qrels:
            ap = compute_ap(qrels[qid], results[qid])
            ap_scores.append(ap)
            q_count += 1
            if q_count <= 10:
                print(f"  Query {qid}: AP = {ap:.6f}")
    
    if q_count > 10:
        print(f"  ... and {q_count - 10} more queries")
    
    if ap_scores:
        map_score = sum(ap_scores) / len(ap_scores)
        print(f"\n  >>> MAP = {map_score:.6f} <<<")
    else:
        print("  No valid queries found")
    
    return map_score

def evaluate_all():
    print("="*60)
    print("EVALUATING ALL RESULTS")
    print("="*60)
    
    result_files = [
        "results_OkapiTF_Unstemmed.txt",
        "results_BM25_Unstemmed.txt",
        "results_OkapiTF_Stemmed.txt",
        "results_BM25_Stemmed.txt",
        "results_Proximity.txt"
    ]
    
    scores = {}
    for f in result_files:
        try:
            scores[f] = evaluate_single(f)
        except FileNotFoundError:
            print(f"\n{f}: NOT FOUND - Run run_experiments.py first")
    
    print("\n" + "="*60)
    print("SUMMARY - MAP SCORES")
    print("="*60)
    for name, score in scores.items():
        print(f"  {name:35} {score:.6f}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        evaluate_single(sys.argv[1])
    else:
        evaluate_all()
