from langchain import hub
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Load the RAG prompt from LangChain hub
prompt = hub.pull("rlm/rag-prompt")

# Load Llama model
llm = OllamaLLM(model="llama3.2")

# Function to format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Wrap format_docs in RunnableLambda to make it chainable
format_docs_runnable = RunnableLambda(format_docs)

def generate_response(retriever, query):
    """Generates an LLM response using retrieved context."""

    # Create a retriever chain with formatting
    retriever_chain = retriever | format_docs_runnable
    print(type(retriever))
    # Create RAG chain for QA
    rag_chain = (
        {"context": retriever_chain, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print(query)
    # # Invoke the chain correctly with both context & question
    response = rag_chain.invoke(query)

    return response
