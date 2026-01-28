import requests
from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 1. Fetch
print("Downloading docs...")
full_text = requests.get("https://nextjs.org").text

# 2. Chunk
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
documents = [Document(page_content=t) for t in text_splitter.split_text(full_text)]

# 3. Fast Embeddings with Phi-3.5
print(f"Starting Ingestion of {len(documents)} chunks...")
embeddings = OllamaEmbeddings(model="phi3.5")

vector_db = None
# This loop gives you a visual progress bar
for doc in tqdm(documents, desc="Embedding Next.js Docs"):
    if vector_db is None:
        vector_db = FAISS.from_documents([doc], embeddings)
    else:
        vector_db.add_documents([doc])

# 4. Save
vector_db.save_local("nextjs_faiss_index")
print("\nSuccess! Index created.")
