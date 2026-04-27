import math
from helpers import SearchHelpers

class RankingModels:
    def __init__(self):
        self.helpers = SearchHelpers()
    
    def score_okapi_tf(self, query_terms, doc_id):
        """
        Okapi TF: TF / (TF + 0.5 + 1.5 * (doc_len/avg_len))
        """
        score = 0.0
        doc_len = self.helpers.get_doc_length(doc_id)
        
        for term in query_terms:
            tf = self.helpers.get_tf(term, doc_id)
            if tf == 0:
                continue
            
            okapi = tf / (tf + 0.5 + 1.5 * (doc_len / self.helpers.avgdl))
            score += okapi
        
        return score
    
    def score_tfidf(self, query_terms, doc_id):
        """
        TF-IDF: Okapi_TF * log(N / DF)
        """
        score = 0.0
        doc_len = self.helpers.get_doc_length(doc_id)
        
        for term in query_terms:
            tf = self.helpers.get_tf(term, doc_id)
            if tf == 0:
                continue
            
            okapi = tf / (tf + 0.5 + 1.5 * (doc_len / self.helpers.avgdl))
            df = self.helpers.get_df(term)
            idf = math.log((self.helpers.N - df + 0.5) / (df + 0.5) + 1.0)
            
            score += okapi * idf
        
        return score
    
    def score_bm25(self, query_terms, doc_id, k1=1.2, b=0.75):
        """
        BM25: IDF * (TF*(k1+1)) / (TF + k1*(1-b + b*len/avg_len))
        """
        score = 0.0
        doc_len = self.helpers.get_doc_length(doc_id)
        
        for term in query_terms:
            tf = self.helpers.get_tf(term, doc_id)
            if tf == 0:
                continue
            
            df = self.helpers.get_df(term)
            idf = math.log((self.helpers.N - df + 0.5) / (df + 0.5) + 1.0)
            
            tf_part = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / self.helpers.avgdl)))
            
            score += idf * tf_part
        
        return score
    
    def score_laplace_lm(self, query_terms, doc_id):
        """
        Laplace Language Model: log((tf + 1) / (doc_len + V))
        """
        score = 0.0
        doc_len = self.helpers.get_doc_length(doc_id)
        
        for term in query_terms:
            tf = self.helpers.get_tf(term, doc_id)
            prob = (tf + 1) / (doc_len + self.helpers.V)
            score += math.log(prob)
        
        return score
    
    def score_jelinek_mercer_lm(self, query_terms, doc_id, lam=0.7):
        """
        Jelinek-Mercer Language Model: log(λ * (tf/len) + (1-λ) * (1/V))
        """
        score = 0.0
        doc_len = self.helpers.get_doc_length(doc_id)
        
        for term in query_terms:
            tf = self.helpers.get_tf(term, doc_id)
            
            p_doc = tf / doc_len if doc_len > 0 else 0
            p_collection = 1.0 / self.helpers.V
            
            prob = lam * p_doc + (1 - lam) * p_collection
            
            if prob > 0:
                score += math.log(prob)
        
        return score

# Test the ranking models
if __name__ == "__main__":
    ranking = RankingModels()
    
    # Test with a sample query
    test_query = "aerodynamic heating"
    test_doc = "1"
    query_terms = test_query.lower().split()
    
    print(f"Testing ranking formulas for query='{test_query}', doc={test_doc}")
    print("-" * 50)
    
    score1 = ranking.score_okapi_tf(query_terms, test_doc)
    score2 = ranking.score_tfidf(query_terms, test_doc)
    score3 = ranking.score_bm25(query_terms, test_doc)
    score4 = ranking.score_laplace_lm(query_terms, test_doc)
    score5 = ranking.score_jelinek_mercer_lm(query_terms, test_doc)
    
    print(f"Okapi TF score:      {score1:.6f}")
    print(f"TF-IDF score:        {score2:.6f}")
    print(f"BM25 score:          {score3:.6f}")
    print(f"Laplace LM score:    {score4:.6f}")
    print(f"Jelinek-Mercer LM:   {score5:.6f}")