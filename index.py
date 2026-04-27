import xml.etree.ElementTree as ET
import re
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

print("=" * 50)
print("STEP 1: Indexing Documents into Elasticsearch")
print("=" * 50)

# Connect to Elasticsearch (runs on your computer)
es = Elasticsearch(["http://localhost:9200"])
print("✓ Connected to Elasticsearch")

# Delete old index if it exists (clean start)
if es.indices.exists(index="cranfield"):
    es.indices.delete(index="cranfield")
    print("✓ Removed old index")

# Create new index with proper settings
es.indices.create(index="cranfield", body={
    "mappings": {
        "properties": {
            "docno": {"type": "keyword"},
            "text": {"type": "text", "term_vector": "yes"},
            "length": {"type": "integer"}
        }
    }
})
print("✓ Created new index 'cranfield'")

# Parse the XML file
print("\nReading cran.all.1400.xml...")
with open(r"C:\Users\HP\Desktop\cranfield\cran.all.1400.xml", "r", encoding="utf-8") as f:
    content = f.read()
    wrapped_content = "<root>" + content + "</root>"
    root = ET.fromstring(wrapped_content)

# Prepare documents for indexing
actions = []
doc_count = 0

for doc in root.findall(".//doc"):
    docno = doc.findtext("docno").strip()
    title = doc.findtext("title", "")
    text = doc.findtext("text", "")
    
    # Combine title and text, convert to lowercase
    full_text = (title + " " + text).lower()
    
    # Clean up whitespace
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    # Count number of words (document length)
    word_count = len(full_text.split())
    
    # Prepare for Elasticsearch
    actions.append({
        "_index": "cranfield",
        "_id": docno,
        "_source": {
            "docno": docno,
            "text": full_text,
            "length": word_count
        }
    })
    doc_count += 1
    
    # Show progress every 100 documents
    if doc_count % 100 == 0:
        print(f"  Processed {doc_count} documents...")

# Send all documents to Elasticsearch
success, _ = bulk(es, actions)
print(f"\n✓ Indexed {success} documents successfully!")

# Wait for Elasticsearch to refresh
time.sleep(2)

# Verify
result = es.count(index="cranfield")
print(f"✓ Verification: {result['count']} documents in index")

print("\n" + "=" * 50)
print("STEP 1 COMPLETE!")
print("=" * 50)