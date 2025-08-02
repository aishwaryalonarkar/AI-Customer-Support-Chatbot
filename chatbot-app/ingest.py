import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Get the absolute path of the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file in the script's directory
dotenv_path = os.path.join(SCRIPT_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

# Get the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure to create a .env file in the chatbot-app directory with your key.")

# Constants using absolute paths
DATA_PATH = os.path.join(SCRIPT_DIR, "data.txt")
DB_DIR = os.path.join(SCRIPT_DIR, "chroma_db")

def main():
    """
    This function performs the following steps:
    1. Loads documents from the specified data path.
    2. Splits the documents into smaller chunks for processing.
    3. Creates a Chroma vector store from the chunks and persists it to disk.
    """
    # 1. Load documents
    print(f"Loading data from {DATA_PATH}...")
    loader = TextLoader(DATA_PATH)
    documents = loader.load()
    if not documents:
        print("No documents found. Exiting.")
        return

    print(f"Loaded {len(documents)} document(s).")

    # 2. Split documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    # 3. Create embeddings and Chroma vector store
    print("Creating embeddings and vector store...")
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    # Create the Chroma vector store and persist it
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    vectordb.persist()
    print(f"Vector store created and persisted at '{DB_DIR}'.")
    print("Ingestion complete!")


if __name__ == "__main__":
    main()
