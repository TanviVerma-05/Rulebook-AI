# Rulebook AI

A grounded Retrieval-Augmented Generation (RAG) system for answering university rulebook questions with traceable evidence.

Rulebook AI is designed to **answer only from the provided rulebook corpus**, refuse questions that are not supported by the corpus, and explicitly surface contradictory rules instead of silently choosing one.

![Rulebook AI Demo](screenshots/rulebook-ai.png)

--- 

## Problem Statement

University rulebooks contain large amounts of information across different documents and formats. A general-purpose LLM may answer questions using information from its training data instead of the actual university rules.

This project builds a checkable RAG system where:

- Answers are grounded in the provided rulebook.
- Every factual answer can be traced to retrieved source evidence.
- Questions outside the corpus are refused.
- Conflicting rules are explicitly identified.
- The system can be evaluated using a reproducible evaluation script.

---

# Key Features

### 1. Grounded RAG Question Answering

A student can ask a question in natural language.

The system retrieves relevant passages from the rulebook corpus and uses those passages as the only evidence for answer generation.

### 2. Three Explicit States

The system distinguishes between three situations:

| State | Meaning |
|---|---|
| `ANSWER` | The corpus contains sufficient evidence to answer the question. |
| `NO_EVIDENCE` | The corpus does not contain sufficient evidence. |
| `CONTRADICTION` | The retrieved evidence contains materially incompatible information. |

### 3. Traceable Evidence

Answers include source information such as:

- Document name
- Section
- Page where applicable
- Retrieved chunk ID

This allows the user to trace an answer back to the underlying rulebook material.

### 4. Contradiction Detection

The system does not silently select one answer when two sources disagree.

Instead, it returns `CONTRADICTION` and displays the conflicting evidence.

### 5. Honest Refusal

Questions unrelated to the available rulebook are refused instead of being answered from general model knowledge.

---

# Corpus

The corpus contains approximately **45,000+ words** of rulebook content, exceeding the required 6,000-word minimum.

The corpus uses multiple formats:

```text
corpus/
├── rulebook.md
├── fee_table.md
├── regulations.pdf
└── contradictions.md
```


# Setup

Follow the steps below to run Rulebook AI locally.

## Prerequisites

Make sure the following are installed:

- Python 3.11+
- Node.js and npm
- Git
- A Gemini API key

---

## 1. Clone the Repository

    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd rulebook-ai

---

## 2. Set Up the Python Environment

Create the Python virtual environment inside `ai_engine`:

    python -m venv ai_engine/venv

### Windows

Activate the environment:

    ai_engine\venv\Scripts\Activate.ps1

If PowerShell blocks script execution, you can directly use the Python executable:

    ai_engine\venv\Scripts\python.exe

---

## 3. Install Python Dependencies

Install the required Python packages:

    pip install google-genai sentence-transformers numpy

The project uses:

- `sentence-transformers` for document and query embeddings
- `numpy` for similarity search
- `google-genai` for Gemini-based grounded answer generation

---

## 4. Configure the Gemini API Key

Create a `.env` file in the project root:

    rulebook-ai/
    └── .env

Add the following:

    GEMINI_API_KEY=your_api_key_here

Replace `your_api_key_here` with your Gemini API key.

**Do not commit the `.env` file to GitHub.**

The repository `.gitignore` already excludes `.env`.

---

## 5. Install Backend Dependencies

Open a terminal in the backend directory:

    cd backend
    npm install

Start the Express backend:

    node server.js

The backend will run on:

    http://localhost:5000

You should see:

    Server running on http://localhost:5000

Keep this terminal running.

---

## 6. Start the Frontend

Open a **new terminal** and move to the frontend directory:

    cd frontend

Install the frontend dependencies:

    npm install

Start the Vite development server:

    npm run dev

Open the URL shown by Vite, typically:

    http://localhost:5173

---

## 7. Run the Application

Once both servers are running, the application works as follows:

    Frontend
    http://localhost:5173
            |
            v
    Node.js + Express
    http://localhost:5000
            |
            v
    Python RAG Pipeline

Enter a question in the Rulebook AI interface and click **Ask Rulebook**.

---

## 8. Run the Evaluation

The repository includes a reproducible evaluation script containing 25 unanswerable questions.

From the project root, run:

    python evaluation/evaluate.py

Expected result:

    Total questions:       25
    Correctly refused:     25
    Incorrect responses:   0
    Refusal accuracy:      100.00%

Detailed results are saved to:

    evaluation/evaluation_results.json

---

## 9. Rebuilding the Index

The document-processing and embedding scripts are located in:

    ai_engine/

If the corpus is modified, the RAG index can be rebuilt using the available indexing and embedding scripts.

Generated embedding data is excluded from Git using `.gitignore`.

---

## Troubleshooting

### Backend cannot start

Make sure Node.js is installed and run:

    cd backend
    npm install
    node server.js

### Python RAG engine cannot start

Make sure the Python virtual environment exists:

    ai_engine/venv/

On Windows, verify that the following file exists:

    ai_engine/venv/Scripts/python.exe

### Gemini API error

Check that `.env` exists in the project root and contains:

    GEMINI_API_KEY=your_api_key_here

### Frontend cannot connect to backend

Make sure the Express server is running on:

    http://localhost:5000

and the frontend is running on the Vite development server.
