# Customer Support Chatbot with RAG

This project is a fully functional Customer Support Chatbot built with Next.js, Python, LangChain, and ChromaDB. It uses the Retrieval-Augmented Generation (RAG) model to answer questions based on a provided set of documents.

## Features

- **Frontend:** A clean, responsive chat interface built with Next.js and Tailwind CSS.
- **Backend:** A powerful RAG pipeline powered by LangChain and a FastAPI server.
- **Vector Store:** Uses ChromaDB for local vector storage and retrieval.
- **Separation of Concerns:** The Next.js frontend communicates with the Python backend via a proxy API route, ensuring a secure and scalable architecture.

## Project Structure

```
/
├── backend/
│   └── main.py         # FastAPI backend with the LangChain RAG pipeline
├── chroma_db/          # Directory for the local Chroma vector store (gitignored)
├── public/             # Next.js public assets
├── src/
│   ├── app/
│   │   ├── api/ask/
│   │   │   └── route.ts  # Next.js API route (proxy to backend)
│   │   ├── layout.tsx
│   │   └── page.tsx      # Frontend chat UI
├── .env.example        # Example environment file
├── data.txt            # Sample FAQ data for ingestion
├── ingest.py           # Python script to process data and create the vector store
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
└── README.md
```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v18 or later)
- [Python](https://www.python.org/downloads/) (v3.9 or later)
- `npm` for Node.js package management
- `pip` for Python package management

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository-url>
cd chatbot-app
```

### 2. Set Up Environment Variables

The application requires an OpenAI API key to function.

1.  Create a `.env` file in the root of the `chatbot-app` directory by copying the example file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```

### 3. Set Up the Backend

1.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *On Windows, use `.venv\Scripts\activate`*

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

### 4. Set Up the Frontend

1.  **Install the Node.js dependencies:**
    ```bash
    npm install
    ```

## Running the Application

You need to run three processes in separate terminals: the data ingestion script (only once), the backend server, and the frontend server.

### Step 1: Ingest the Data

Before starting the servers, you must run the ingestion script to populate the Chroma vector database.

- **Make sure your virtual environment is activated.**
- **From the `chatbot-app` root directory, run:**

```bash
python ingest.py
```

You should see output indicating that the data has been loaded, split, and stored in the `chroma_db` directory. You only need to do this once unless you change the `data.txt` file.

### Step 2: Start the Backend Server

- **Make sure your virtual environment is activated.**
- **From the `chatbot-app` root directory, run:**

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The FastAPI server should now be running on `http://127.0.0.1:8000`.

### Step 3: Start the Frontend Server

- **In a new terminal, from the `chatbot-app` root directory, run:**

```bash
npm run dev
```

The Next.js development server will start, typically on `http://localhost:3000`.

### Step 4: Open the Chatbot

Open [http://localhost:3000](http://localhost:3000) in your browser. 
