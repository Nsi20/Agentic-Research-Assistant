import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- LLM provider (GROQ) ---
from langchain_groq import ChatGroq

# --- Core LangChain Tools ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def load_document(file_path):
    """Load a text or markdown document."""
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    return documents


def split_text(documents):
    """Split large text into chunks for processing."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)


def create_llm():
    """Initialize the Groq LLM."""
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="mixtral-8x7b-32768",   # You can change to llama3-70b if you want
        temperature=0.2
    )


def build_chain(llm):
    """Create a prompt + model + output parser chain."""

    prompt = ChatPromptTemplate.from_template("""
You are a helpful research assistant.
Summarize the following text clearly and concisely:

TEXT:
{input}
""")

    output_parser = StrOutputParser()

    # Chain = prompt → LLM → parser
    return prompt | llm | output_parser


def run_analysis(file_path):
    # 1. Load
    documents = load_document(file_path)

    # 2. Split
    chunks = split_text(documents)

    # 3. Create LLM + chain
    llm = create_llm()
    chain = build_chain(llm)

    print("\n=== SUMMARY OUTPUT ===\n")

    # 4. Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---\n")
        response = chain.invoke({"input": chunk.page_content})
        print(response)


if __name__ == "__main__":
    # Change this to your file
    file_path = "input.txt"  # Example file
    run_analysis(file_path)
