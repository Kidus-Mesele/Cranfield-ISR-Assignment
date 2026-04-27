from elasticsearch import Elasticsearch
from queries import get_queries

print("Running Elasticsearch Built-in BM25...")

es = Elasticsearch(["http://localhost:9200"])
queries = get_queries()

with open("results_ES_Builtin.txt", "w") as out:
    for query in queries:
        qid = query["id"]
        query_text = query["text"]
        
        # Use Elasticsearch's built-in search
        resp = es.search(index="cranfield", body={
            "size": 100,
            "query": {
                "match": {
                    "text": query_text
                }
            }
        })
        
        for rank, hit in enumerate(resp["hits"]["hits"], 1):
            out.write(f"{qid} Q0 {hit['_id']} {rank} {hit['_score']:.6f} ES_Builtin\n")

print("✓ Results saved to results_ES_Builtin.txt")