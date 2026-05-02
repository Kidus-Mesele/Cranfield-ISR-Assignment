import xml.etree.ElementTree as ET
import re

def get_queries():
    """Extract all queries from cran.qry.xml"""
    tree = ET.parse("cran.qry.xml")
    root = tree.getroot()
    
    queries = []
    for topic in root.findall(".//top"):
        num = topic.findtext("num").strip()
        title = topic.findtext("title").strip()
        
        # Clean the query text
        title = title.lower()
        title = re.sub(r'\s+', ' ', title).strip()
        title = re.sub(r'[^\w\s]', '', title)  # Remove punctuation
        
        queries.append({
            "id": num,
            "text": title,
            "terms": title.split()
        })
    
    return queries

# Test
if __name__ == "__main__":
    queries = get_queries()
    print(f"Loaded {len(queries)} queries")
    print("\nFirst 5 queries:")
    for i, q in enumerate(queries[:5], 1):
        print(f"{i}. Query {q['id']}: {q['text'][:80]}...")
