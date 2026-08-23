import os
import glob
import PyPDF2
import chromadb
from chromadb.utils import embedding_functions

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_metadata_for_file(filename):
    basename = os.path.basename(filename)
    meta = {
        "document": basename,
        "source_type": "unknown",
        "authority_level": 4,
        "status": "UNKNOWN",
        "account_id": "",
        "customer_name": ""
    }
    if "CURRENT" in basename and "Policy" in basename:
        meta["source_type"] = "policy"
        meta["authority_level"] = 2
        meta["status"] = "CURRENT"
    elif "DEPRECATED" in basename:
        meta["source_type"] = "policy"
        meta["authority_level"] = 2
        meta["status"] = "DEPRECATED"
    elif "SOP" in basename:
        meta["source_type"] = "sop"
        meta["authority_level"] = 2
        meta["status"] = "CURRENT"
    elif "Product" in basename:
        meta["source_type"] = "product_docs"
        meta["authority_level"] = 3
        meta["status"] = "CURRENT"
    elif "Northstar" in basename:
        meta["source_type"] = "agreement"
        meta["authority_level"] = 1
        meta["status"] = "ACTIVE"
        meta["account_id"] = "ACCT-001"
        meta["customer_name"] = "Northstar Logistics"
    elif "LumenWorks" in basename:
        meta["source_type"] = "agreement"
        meta["authority_level"] = 1
        meta["status"] = "ACTIVE"
        meta["account_id"] = "ACCT-002"
        meta["customer_name"] = "LumenWorks"
        
    return meta

def main():
    client = chromadb.PersistentClient(path="./chroma_db")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="parcelpilot_docs", embedding_function=sentence_transformer_ef)
    
    pdf_files = glob.glob("../data/*.pdf")
    
    for pdf_file in pdf_files:
        print(f"Ingesting {pdf_file}...")
        text = extract_text_from_pdf(pdf_file)
        chunks = chunk_text(text)
        
        meta_template = get_metadata_for_file(pdf_file)
        
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{meta_template['document']}_chunk_{i}"
            meta = meta_template.copy()
            meta["chunk_id"] = chunk_id
            
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append(meta)
            
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(chunks)} chunks for {pdf_file}")

if __name__ == "__main__":
    main()
