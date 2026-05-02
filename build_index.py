import re
from collections import defaultdict
from tokenizer import tokenize

STOPWORDS = set(open("stopwords.txt").read().splitlines())

class InvertedIndex:
    def __init__(self, name, use_stemming):
        self.name = name
        self.use_stemming = use_stemming
        self.term_to_id = {}
        self.term_info = {}
        self.doc_to_id = {}
        self.id_to_doc = {}
        self.doc_lengths = {}
        self.next_term_id = 1
        self.next_doc_id = 1
        
        if use_stemming:
            from stemming.porter2 import stem
            self.stem = stem
        else:
            self.stem = lambda x: x
    
    def get_term_id(self, term):
        term = self.stem(term)
        if term not in self.term_to_id:
            self.term_to_id[term] = self.next_term_id
            self.term_info[self.next_term_id] = {"df": 0, "ttf": 0, "postings": []}
            self.next_term_id += 1
        return self.term_to_id[term]
    
    def get_doc_id(self, docno):
        if docno not in self.doc_to_id:
            self.doc_to_id[docno] = self.next_doc_id
            self.id_to_doc[self.next_doc_id] = docno
            self.next_doc_id += 1
        return self.doc_to_id[docno]
    
    def add_document(self, docno, text):
        doc_id = self.get_doc_id(docno)
        tokens = tokenize(text)
        
        term_positions = defaultdict(list)
        for token, pos in tokens:
            token = self.stem(token)
            if token in STOPWORDS:
                continue
            term_positions[token].append(pos)
        
        self.doc_lengths[doc_id] = sum(len(p) for p in term_positions.values())
        
        for term, positions in term_positions.items():
            term_id = self.get_term_id(term)
            tf = len(positions)
            self.term_info[term_id]["ttf"] += tf
            self.term_info[term_id]["postings"].append((doc_id, tf, positions))
    
    def save(self):
        for term_id in self.term_info:
            self.term_info[term_id]["df"] = len(self.term_info[term_id]["postings"])
            self.term_info[term_id]["postings"].sort(key=lambda x: x[1], reverse=True)
        
        with open(f"{self.name}_index.txt", "w") as f:
            for term_id, info in sorted(self.term_info.items()):
                line = f"{term_id},{info['df']},{info['ttf']}:"
                postings_list = []
                for doc_id, tf, positions in info["postings"]:
                    pos_str = ",".join(str(p) for p in positions)
                    postings_list.append(f"{doc_id},{tf},{pos_str}")
                line += ";".join(postings_list)
                f.write(line + "\n")
        
        with open(f"{self.name}_term_map.txt", "w") as f:
            for term, tid in sorted(self.term_to_id.items()):
                f.write(f"{term},{tid}\n")
        
        with open(f"{self.name}_doc_map.txt", "w") as f:
            for docno, did in sorted(self.doc_to_id.items(), key=lambda x: x[1]):
                f.write(f"{docno},{did}\n")
        
        with open(f"{self.name}_doc_lengths.txt", "w") as f:
            for did, length in sorted(self.doc_lengths.items()):
                f.write(f"{did},{length}\n")

def parse_cranfield():
    with open("data/cran.all.1400.xml", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove XML declaration if present
    content = re.sub(r'<\?xml.*?\?>', '', content)
    
    # Find all <doc> ... </doc> blocks
    pattern = r'<doc>(.*?)</doc>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        docno_match = re.search(r'<docno>(.*?)</docno>', match, re.DOTALL)
        title_match = re.search(r'<title>(.*?)</title>', match, re.DOTALL)
        text_match = re.search(r'<text>(.*?)</text>', match, re.DOTALL)
        
        if docno_match is None:
            continue
        
        docno = docno_match.group(1).strip()
        title = title_match.group(1).strip() if title_match else ""
        text = text_match.group(1).strip() if text_match else ""
        
        # Clean text
        title = re.sub(r'\s+', ' ', title)
        text = re.sub(r'\s+', ' ', text)
        
        if docno:
            yield docno, title + " " + text

def main():
    print("="*50)
    print("BUILDING INVERTED INDEXES")
    print("="*50)
    
    print("\nBuilding UNSTEMMED index (stopwords removed, no stemming)...")
    idx1 = InvertedIndex("unstemmed", use_stemming=False)
    count = 0
    for docno, text in parse_cranfield():
        idx1.add_document(docno, text)
        count += 1
        if count % 200 == 0:
            print(f"  Processed {count} documents...")
    idx1.save()
    print(f"  Documents: {len(idx1.doc_to_id)}")
    print(f"  Unique terms: {len(idx1.term_to_id)}")
    
    print("\nBuilding STEMMED index (stopwords removed, Porter2 stemming)...")
    idx2 = InvertedIndex("stemmed", use_stemming=True)
    count = 0
    for docno, text in parse_cranfield():
        idx2.add_document(docno, text)
        count += 1
        if count % 200 == 0:
            print(f"  Processed {count} documents...")
    idx2.save()
    print(f"  Documents: {len(idx2.doc_to_id)}")
    print(f"  Unique terms: {len(idx2.term_to_id)}")
    
    print("\n" + "="*50)
    print("INDEX FILES CREATED!")
    print("="*50)

if __name__ == "__main__":
    main()