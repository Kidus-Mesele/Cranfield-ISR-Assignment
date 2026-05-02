from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

# Your settings (already correct)
INDEX_NAME = "cranfield"
FIELD_NAME = "text"

queries = [
    ('Causes of world war 2', '151801'),
    ('Battles won by USA in World War 2', '151802'),
    ('Battle of Stalingrad', '151803')
]

def createRankList(query, qid):
    es = Elasticsearch("http://localhost:9200")
    
    s = Search(using=es, index=INDEX_NAME).query("match", **{FIELD_NAME: query})
    
    res = s[0:1000].execute()
    
    print(f"  Query '{query[:30]}...' found {len(res.hits)} results")
    
    with open('rankList.txt', 'a') as f:
        for i, h in enumerate(res.hits, start=1):
            # Use rank position as document ID (mock approach)
            doc_id = str(i)
            line = f"{qid} Q0 {doc_id} {i} {h.meta.score} Exp\n"
            f.write(line)

def main():
    # Clear old file
    open('rankList.txt', 'w').close()
    
    print("Running queries...")
    print("-"*40)
    
    for query, qid in queries:
        createRankList(query, qid)
    
    print("-"*40)
    print("Done! Created rankList.txt")

if __name__ == "__main__":
    main()