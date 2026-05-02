import re
from index_reader import IndexReader
from ranking import Ranker

STOPWORDS = set(open("stopwords.txt").read().splitlines())

def get_queries():
    with open("data/cran.qry.xml", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove XML declaration
    content = re.sub(r'<\?xml.*?\?>', '', content)
    
    # Find all <top> ... </top> blocks
    pattern = r'<top>(.*?)</top>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    queries = []
    for match in matches:
        num_match = re.search(r'<num>\s*(\d+)\s*</num>', match)
        title_match = re.search(r'<title>(.*?)</title>', match, re.DOTALL)
        
        if num_match and title_match:
            qid = num_match.group(1)
            text = title_match.group(1).strip().lower()
            text = re.sub(r'\s+', ' ', text)
            queries.append((qid, text))
    
    print(f"Loaded {len(queries)} queries")
    return queries

def process_query(text, use_stemming):
    from tokenizer import tokenize
    from stemming.porter2 import stem
    
    terms = []
    for token, _ in tokenize(text):
        if use_stemming:
            token = stem(token)
        if token in STOPWORDS:
            continue
        terms.append(token)
    return terms

def run_model(index_name, model_name, score_func, use_stemming):
    print(f"\nRunning {model_name} on {index_name}...")
    
    reader = IndexReader(index_name)
    ranker = Ranker(reader)
    queries = get_queries()
    all_docs = reader.get_all_doc_ids()
    
    if not all_docs:
        print(f"  ERROR: No documents found")
        return
    
    filename = f"results_{model_name}.txt"
    processed = 0
    with open(filename, "w") as out:
        for qid, qtext in queries:
            terms = process_query(qtext, use_stemming)
            if not terms:
                continue
            
            scores = []
            for doc_id in all_docs:
                score = score_func(ranker, terms, doc_id)
                if score > 0:
                    docno = reader.get_docno(doc_id)
                    if docno:
                        scores.append((docno, score))
            
            scores.sort(key=lambda x: x[1], reverse=True)
            for rank, (docno, score) in enumerate(scores[:100], 1):
                out.write(f"{qid} Q0 {docno} {rank} {score:.6f} {model_name}\n")
            
            processed += 1
            if processed % 50 == 0:
                print(f"  Processed {processed} queries...")
    
    print(f"  Saved {filename}")

def main():
    print("="*60)
    print("HOMEWORK 2 - RUNNING EXPERIMENTS")
    print("="*60)
    
    # Test queries first
    print("\nTesting query loading...")
    queries = get_queries()
    if not queries:
        print("ERROR: No queries loaded!")
        return
    print(f"Success! Loaded {len(queries)} queries")
    print(f"First query: ID={queries[0][0]}, text={queries[0][1][:50]}...")
    
    # 5 experiments
    run_model("unstemmed", "OkapiTF_Unstemmed", 
              lambda r, t, d: r.okapi_tf(t, d), False)
    
    run_model("unstemmed", "BM25_Unstemmed",
              lambda r, t, d: r.bm25(t, d), False)
    
    run_model("stemmed", "OkapiTF_Stemmed",
              lambda r, t, d: r.okapi_tf(t, d), True)
    
    run_model("stemmed", "BM25_Stemmed",
              lambda r, t, d: r.bm25(t, d), True)
    
    run_model("unstemmed", "Proximity",
              lambda r, t, d: r.proximity(t, d), False)
    
    print("\n" + "="*60)
    print("ALL EXPERIMENTS COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()
