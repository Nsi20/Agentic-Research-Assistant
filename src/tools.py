# src/tools.py

import os
import chromadb
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from crewai_tools import TavilySearchTool, FileWriterTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any

# --- Knowledge Storage Tool Definition ---

class StoreKnowledgeInput(BaseModel):
    content: str = Field(description="Content to store in the knowledge base")

class StoreKnowledgeTool(BaseTool):
    name: str = "Knowledge Storage Tool"
    description: str = "Stores research findings, facts, and data into the internal vector database. Use this tool to save useful information found during research."
    args_schema: type[BaseModel] = StoreKnowledgeInput
    vector_store: Any = Field(description="The vector store to use", exclude=True)
    
    def _run(self, content: str) -> str:
        self.vector_store.add_texts([content])
        return "Content successfully stored in knowledge base."

# --- Retrieval Tool Definition ---

class RetrievalInput(BaseModel):
    query: str = Field(description="Query to search the knowledge base")

class RetrievalToolClass(BaseTool):
    name: str = "Internal Knowledge Retrieval Tool"
    description: str = "Search and retrieve research snippets from the internal knowledge base. Useful for the Analysis Agent."
    args_schema: type[BaseModel] = RetrievalInput
    vector_store: Any = Field(description="The vector store to use", exclude=True)
    
    def _run(self, query: str) -> str:
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])

# --- Initialization Function ---

def initialize_tools():
    """
    Initializes and returns all tools and the vector store.
    This function should be called inside the app to avoid blocking imports.
    """
    # 1. Configure Search and File Tools
    research_tool = TavilySearchTool(
        config={"max_results": 8, "api_key": os.getenv("TAVILY_API_KEY")}
    )

    citation_tool = TavilySearchTool(
        config={"max_results": 3, "api_key": os.getenv("TAVILY_API_KEY")}
    )

    file_writer_tool = FileWriterTool()

    # 2. Configure ChromaDB and Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    DB_DIR = "./chroma_db"
    COLLECTION_NAME = "research_knowledge_base"

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )

    # 3. Instantiate Custom Tools with vector_store
    store_knowledge_tool = StoreKnowledgeTool(vector_store=vector_store)
    retrieval_tool = RetrievalToolClass(vector_store=vector_store)

    return {
        "research_tool": research_tool,
        "citation_tool": citation_tool,
        "file_writer_tool": file_writer_tool,
        "store_knowledge_tool": store_knowledge_tool,
        "retrieval_tool": retrieval_tool,
        "vector_store": vector_store,
        "embeddings": embeddings
    }

def clear_db(vector_store):
    """Clears existing collection before a new run."""
    try:
        vector_store.delete_collection()
        print("Database cleared for new run.")
    except Exception as e:
        print(f"Note: Database clear skipped or failed: {e}")

def get_db_path():
    return "./chroma_db"
