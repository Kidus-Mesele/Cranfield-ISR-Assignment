import sys
from collections import defaultdict

def load_qrels(qrel_file):
    qrels = defaultdict(dict)
    with open(qrel_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                qid, _, docid, rel = parts
                qrels[qid][docid] = int(rel)
    return qrels

def load_results(results_file):
    results = defaultdict(list)
    with open(results_file, 'r') as f:
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

def evaluate_all():
    qrels = load_qrels("data/cranqrel.trec.txt")
    
    models = ['OkapiTF', 'TFIDF', 'BM25', 'Laplace', 'JelinekMercer', 'ES_Builtin', 'ML_Linear']
    
    print("\n" + "=" * 50)
    print("MAP SCORES")
    print("=" * 50)
    
    scores = {}
    for model in models:
        if model == 'ML_Linear':
            results_file = "results_ML_Linear.txt"
        else:
            results_file = f"results/results_{model}.txt"
        
        try:
            results = load_results(results_file)
            ap_sum = 0
            q_count = 0
            for qid, retrieved in results.items():
                if qid in qrels:
                    ap = compute_ap(qrels[qid], retrieved)
                    ap_sum += ap
                    q_count += 1
            map_score = ap_sum / q_count if q_count > 0 else 0
            scores[model] = map_score
            print(f"{model:20} MAP = {map_score:.6f}")
        except FileNotFoundError:
            print(f"{model:20} File not found")
    
    print("\n" + "=" * 50)
    print(f"Best Model: {max(scores, key=scores.get)}")
    print(f"ML Improvement: {(scores.get('ML_Linear', 0) - scores.get('BM25', 0)) * 100:.2f}%")
    print("=" * 50)

if __name__ == "__main__":
    evaluate_all()