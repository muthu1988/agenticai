from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Load local model and embeddings
llm = OllamaLLM(model="codellama")
embeddings = OllamaEmbeddings(model="codellama")

# Load the FAISS index (allow_dangerous_deserialization is required for local loading)
vector_db = FAISS.load_local("nextjs_faiss_index", embeddings, allow_dangerous_deserialization=True)

def review_nextjs_code(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    print(f"--- Raw Code ---")
    print(code)

    # Find relevant docs
    docs = vector_db.similarity_search(code, k=3)
    context = "\n---\n".join([d.page_content for d in docs])
    
    prompt = f"Using this Next.js context:\n{context}\n\nReview this code:\n{code}"
    return llm.invoke(prompt)

# Test it
print(review_nextjs_code("code.ts"))
