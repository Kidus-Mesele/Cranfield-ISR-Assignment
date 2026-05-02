import math
from collections import defaultdict

class Ranker:
    def __init__(self, reader):
        self.r = reader
    
    def okapi_tf(self, terms, doc_id):
        score = 0.0
        doc_len = self.r.get_doc_length(doc_id)
        if doc_len == 0:
            return 0.0
        
        for term in terms:
            tf = self.r.get_tf(term, doc_id)
            if tf == 0:
                continue
            score += tf / (tf + 0.5 + 1.5 * (doc_len / self.r.avgdl))
        return score
    
    def bm25(self, terms, doc_id, k1=1.2, b=0.75):
        score = 0.0
        doc_len = self.r.get_doc_length(doc_id)
        if doc_len == 0:
            return 0.0
        
        for term in terms:
            tf = self.r.get_tf(term, doc_id)
            if tf == 0:
                continue
            
            df = self.r.get_df(term)
            if df == 0:
                continue
            
            idf = math.log((self.r.N - df + 0.5) / (df + 0.5) + 1.0)
            tf_part = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / self.r.avgdl)))
            score += idf * tf_part
        return score
    
    def proximity(self, terms, doc_id, c=1500):
        positions = {}
        for term in terms:
            tf, pos = self.r.get_tf_positions(term, doc_id)
            if tf > 0 and pos:
                positions[term] = pos
        
        if len(positions) < 2:
            return 0.0
        
        all_pos = []
        for term, pos_list in positions.items():
            for p in pos_list:
                all_pos.append((p, term))
        all_pos.sort(key=lambda x: x[0])
        
        term_count = defaultdict(int)
        unique_terms = len(positions)
        left = 0
        min_span = float('inf')
        
        for right in range(len(all_pos)):
            term_count[all_pos[right][1]] += 1
            
            while len(term_count) == unique_terms and left <= right:
                span = all_pos[right][0] - all_pos[left][0]
                if span < min_span:
                    min_span = span
                
                term_count[all_pos[left][1]] -= 1
                if term_count[all_pos[left][1]] == 0:
                    del term_count[all_pos[left][1]]
                left += 1
        
        if min_span == float('inf'):
            return 0.0
        
        doc_len = self.r.get_doc_length(doc_id)
        if doc_len == 0:
            return 0.0
        
        return (c - min_span) * len(terms) / (doc_len + self.r.V)