from elasticsearch import Elasticsearch
import math

class SearchHelpers:
    def __init__(self):
        self.es = Elasticsearch(["http://localhost:9200"])
        self.index = "cranfield"
        
        print("Loading search helpers...")
        
        # Get total number of documents (N)
        result = self.es.count(index=self.index)
        self.N = result["count"]
        print(f"  Total documents (N): {self.N}")
        
        # Get average document length (avgdl)
        resp = self.es.search(index=self.index, body={
            "size": 0,
            "aggs": {"avg_length": {"avg": {"field": "length"}}}
        })
        self.avgdl = resp["aggregations"]["avg_length"]["value"]
        print(f"  Average document length (avgdl): {self.avgdl:.2f}")
        
        # Estimate vocabulary size (V) - total unique words
        resp = self.es.search(index=self.index, body={
            "size": 0,
            "aggs": {"total_terms": {"sum": {"field": "length"}}}
        })
        total_terms = resp["aggregations"]["total_terms"]["value"]
        self.V = total_terms
        print(f"  Approximate vocabulary size (V): {self.V}")
        
        print("✓ Helpers ready!\n")
    
    def get_tf(self, term, doc_id):
        """Get Term Frequency: How many times does 'term' appear in document?"""
        try:
            tv = self.es.termvectors(index=self.index, id=doc_id, fields=["text"])
            if "term_vectors" in tv and "text" in tv["term_vectors"]:
                terms = tv["term_vectors"]["text"]["terms"]
                return terms.get(term, {}).get("term_freq", 0)
        except:
            pass
        return 0
    
    def get_df(self, term):
        """Get Document Frequency: In how many documents does 'term' appear?"""
        try:
            resp = self.es.search(index=self.index, body={
                "size": 0,
                "query": {"match": {"text": term}}
            })
            return resp["hits"]["total"]["value"]
        except:
            return 1
    
    def get_doc_length(self, doc_id):
        """Get the length (word count) of a document"""
        resp = self.es.get(index=self.index, id=doc_id, _source=["length"])
        return resp["_source"]["length"]
    
    def get_all_doc_ids(self):
        """Get list of all document IDs in the index"""
        resp = self.es.search(index=self.index, body={"size": 10000, "_source": ["docno"]})
        return [hit["_id"] for hit in resp["hits"]["hits"]]

# Quick test
if __name__ == "__main__":
    helpers = SearchHelpers()
    
    # Test with a sample term
    test_term = "aerodynamic"
    test_doc = "1"
    
    tf = helpers.get_tf(test_term, test_doc)
    df = helpers.get_df(test_term)
    print(f"Test: term='{test_term}'")
    print(f"  TF in doc {test_doc}: {tf}")
    print(f"  DF across all docs: {df}")
    print(f"  Doc length of doc {test_doc}: {helpers.get_doc_length(test_doc)}")
    print(f"  Total docs in index: {helpers.N}")