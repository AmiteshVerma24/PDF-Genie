from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.schema import Document

# Initialize the embedding model
embeddings = OllamaEmbeddings(model="llama3.2")

def get_embedding(text):
    """Converts text into vector embedding and returns a retriever."""
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_text(text)  # Splitting raw text

    # Create Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    print(f"Documents:- {documents}")
    # Store embeddings in Chroma
    database = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="./chroma_db"
    )
    retriever = database.as_retriever()
    return retriever

def search_query(query, retriever, k=3):
    """Searches the database for the most relevant documents."""
    results = retriever.get_relevant_documents(query, k=k)
    return [doc.page_content for doc in results]