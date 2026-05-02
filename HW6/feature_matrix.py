import csv
from collections import defaultdict

def load_results(results_file):
    results = defaultdict(list)
    with open(results_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 6:
                qid = parts[0]
                docno = parts[2]
                score = float(parts[4])
                results[qid].append((docno, score))
    return results

def load_qrels(qrel_file):
    qrels = defaultdict(dict)
    with open(qrel_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                qid, _, docno, rel = parts
                qrels[qid][docno] = int(rel)
    return qrels

def create_feature_matrix(result_files, qrel_file, output_file):
    print("Loading result files...")
    all_results = {}
    for name, filepath in result_files.items():
        all_results[name] = load_results(filepath)
        print(f"  Loaded {name}: {len(all_results[name])} queries")
    
    print("\nLoading qrels...")
    qrels_data = load_qrels(qrel_file)
    print(f"  Loaded {len(qrels_data)} queries")
    
    first_model = list(all_results.keys())[0]
    all_pairs = []
    for qid, docs in all_results[first_model].items():
        for docno, _ in docs[:100]:
            all_pairs.append((qid, docno))
    print(f"  Total pairs: {len(all_pairs)}")
    
    rows = []
    for qid, docno in all_pairs:
        row = {'qid_doc': f"{qid}-{docno}", 'qid': qid, 'docno': docno}
        for name, results in all_results.items():
            score = 0.0
            if qid in results:
                for d, s in results[qid]:
                    if d == docno:
                        score = s
                        break
            row[name] = score
        label = 0
        if qid in qrels_data and docno in qrels_data[qid]:
            label = qrels_data[qid][docno]
        row['label'] = label
        rows.append(row)
    
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['qid_doc', 'qid', 'docno'] + list(result_files.keys()) + ['label']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\nFeature matrix saved to {output_file}")
    print(f"  Rows: {len(rows)}")
    print(f"  Positive: {sum(1 for r in rows if r['label'] == 1)}")
    print(f"  Negative: {sum(1 for r in rows if r['label'] == 0)}")
    return rows

if __name__ == "__main__":
    result_files = {
        'OkapiTF': 'results/results_OkapiTF.txt',
        'TFIDF': 'results/results_TFIDF.txt',
        'BM25': 'results/results_BM25.txt',
        'Laplace': 'results/results_Laplace.txt',
        'JelinekMercer': 'results/results_JelinekMercer.txt',
        'ES_Builtin': 'results/results_ES_Builtin.txt'
    }
    create_feature_matrix(result_files, "data/cranqrel.trec.txt", "feature_matrix.csv")