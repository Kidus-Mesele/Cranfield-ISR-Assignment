"""
Parse 20 Newsgroups Dataset from Kaggle
Each file contains multiple documents with headers
"""

import os
import re

def parse_20newsgroups(data_folder):
    """
    Parse all text files in the folder
    Each document starts with "Newsgroup:" header
    """
    documents = []
    labels = []
    doc_ids = []
    
    # Get all .txt files (skip list.csv)
    txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
    
    print(f"Found {len(txt_files)} newsgroup files")
    
    for filename in txt_files:
        # Newsgroup name is filename without .txt
        newsgroup = filename.replace('.txt', '')
        filepath = os.path.join(data_folder, filename)
        
        print(f"  Parsing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Split by "Newsgroup:" pattern (each document starts with this)
        # Using regex to find all document boundaries
        documents_raw = re.split(r'\n(?=Newsgroup:)', content)
        
        file_doc_count = 0
        for doc in documents_raw:
            if not doc.strip():
                continue
            
            # Extract document ID (optional)
            doc_id_match = re.search(r'Document_id:\s*(\d+)', doc)
            doc_id = doc_id_match.group(1) if doc_id_match else "unknown"
            
            # Extract the text content (after headers)
            # Headers end with a blank line
            lines = doc.split('\n')
            
            # Find where content starts (after the blank line)
            content_start = 0
            for i, line in enumerate(lines):
                if line.strip() == '':
                    content_start = i + 1
                    break
            
            # Join the content lines
            doc_text = ' '.join(lines[content_start:]).strip()
            
            # Clean up the text (remove extra whitespace)
            doc_text = re.sub(r'\s+', ' ', doc_text)
            
            if doc_text and len(doc_text) > 50:  # Only keep documents with substantial text
                documents.append(doc_text)
                labels.append(newsgroup)
                doc_ids.append(doc_id)
                file_doc_count += 1
        
        print(f"    Extracted {file_doc_count} documents")
    
    return documents, labels, doc_ids


def main():
    print("="*60)
    print("Parsing 20 Newsgroups Dataset (Kaggle)")
    print("="*60)
    
    data_folder = "20_Newsgroups"
    
    print("\n[1] Scanning folder...")
    print(f"    Folder: {data_folder}")
    
    print("\n[2] Parsing files...")
    documents, labels, doc_ids = parse_20newsgroups(data_folder)
    
    print(f"\n[3] Summary:")
    print(f"    Total documents: {len(documents)}")
    print(f"    Unique newsgroups: {len(set(labels))}")
    print(f"    Newsgroups: {', '.join(sorted(set(labels)))}")
    
    # Show distribution
    print("\n[4] Documents per newsgroup:")
    from collections import Counter
    label_counts = Counter(labels)
    for label, count in sorted(label_counts.items()):
        print(f"    {label}: {count}")
    
    # Show sample
    print("\n[5] Sample document:")
    print(f"    Newsgroup: {labels[0]}")
    print(f"    Document ID: {doc_ids[0]}")
    print(f"    Preview: {documents[0][:300]}...")
    
    # Save parsed data for reuse
    import pickle
    with open('newsgroups_data.pkl', 'wb') as f:
        pickle.dump({
            'documents': documents,
            'labels': labels,
            'doc_ids': doc_ids
        }, f)
    
    print("\n[6] Saved to newsgroups_data.pkl")
    print("\n" + "="*60)
    print("PARSING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()