import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Load environment variables from the parent directory's .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Check for OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure to create a .env file in the root directory with your key.")

# Constants for file paths
# The script is in chatbot-app/backend/main.py
# The Chroma DB is in chatbot-app/chroma_db
# The .env file is in chatbot-app/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT_DIR, "chroma_db")

# --- FastAPI App Initialization ---
app = FastAPI(title="Customer Support Chatbot API")

# CORS Middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- LangChain Setup ---
# Initialize embeddings and Chroma DB
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# Check if the database directory exists before loading
if not os.path.exists(DB_DIR):
    raise FileNotFoundError(f"Chroma DB directory not found at {DB_DIR}. Please run ingest.py first from the root directory.")

vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever()

# Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(openai_api_key=api_key),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

# --- API Endpoints ---
class Query(BaseModel):
    question: str

@app.post("/api/ask")
async def ask_question(query: Query):
    """
    Accepts a question, processes it with the RAG chain, and returns the answer.
    """
    if not query.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        llm_response = qa_chain(query.question)
        return {"answer": llm_response["result"].strip(), "source_documents": llm_response["source_documents"]}
    except Exception as e:
        # Log the exception for debugging
        print(f"Error during QA chain processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the question.")

@app.get("/")
def read_root():
    return {"message": "API is running. Use the /api/ask endpoint to ask questions."}

# To run this app:
# 1. Make sure you are in the 'chatbot-app' directory.
# 2. Activate the virtual environment: source .venv/bin/activate
# 3. Run uvicorn: uvicorn backend.main:app --reload --port 8000
