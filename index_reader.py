class IndexReader:
    def __init__(self, prefix):
        self.prefix = prefix
        
        # Load term map
        self.term_to_id = {}
        with open(f"{prefix}_term_map.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    self.term_to_id[parts[0]] = int(parts[1])
        
        # Load doc map
        self.doc_to_id = {}
        self.id_to_doc = {}
        with open(f"{prefix}_doc_map.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    self.doc_to_id[parts[0]] = int(parts[1])
                    self.id_to_doc[int(parts[1])] = parts[0]
        
        # Load doc lengths
        self.doc_lengths = {}
        with open(f"{prefix}_doc_lengths.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    self.doc_lengths[int(parts[0])] = int(parts[1])
        
        # Load inverted index
        self.inverted = {}
        with open(f"{prefix}_index.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                
                header, postings_str = line.split(":", 1)
                header_parts = header.split(",")
                if len(header_parts) != 3:
                    continue
                
                tid = int(header_parts[0])
                df = int(header_parts[1])
                ttf = int(header_parts[2])
                
                postings = []
                if postings_str:
                    for posting in postings_str.split(";"):
                        if not posting:
                            continue
                        posting_parts = posting.split(",")
                        if len(posting_parts) >= 2:
                            doc_id = int(posting_parts[0])
                            tf = int(posting_parts[1])
                            positions = [int(p) for p in posting_parts[2:] if p]
                            postings.append((doc_id, tf, positions))
                
                self.inverted[tid] = {"df": df, "ttf": ttf, "postings": postings}
        
        # Global statistics
        self.N = len(self.doc_lengths)
        self.avgdl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0
        self.V = len(self.term_to_id)
        
        print(f"Loaded {prefix}: {self.N} docs, {self.V} terms, avgdl={self.avgdl:.2f}")
    
    def get_term_id(self, term):
        return self.term_to_id.get(term)
    
    def get_docno(self, doc_id):
        return self.id_to_doc.get(doc_id)
    
    def get_doc_length(self, doc_id):
        return self.doc_lengths.get(doc_id, 0)
    
    def get_tf(self, term, doc_id):
        tid = self.get_term_id(term)
        if not tid or tid not in self.inverted:
            return 0
        for did, tf, _ in self.inverted[tid]["postings"]:
            if did == doc_id:
                return tf
        return 0
    
    def get_tf_positions(self, term, doc_id):
        tid = self.get_term_id(term)
        if not tid or tid not in self.inverted:
            return 0, []
        for did, tf, pos in self.inverted[tid]["postings"]:
            if did == doc_id:
                return tf, pos
        return 0, []
    
    def get_df(self, term):
        tid = self.get_term_id(term)
        if not tid or tid not in self.inverted:
            return 0
        return self.inverted[tid]["df"]
    
    def get_all_doc_ids(self):
        return list(self.doc_lengths.keys())