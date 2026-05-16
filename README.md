# Multisource RAG Research Pipeline

A Python retrieval-augmented generation (RAG) workflow that uses OpenAI vector stores and semantic retrieval to answer JSON structured questions using user uploaded content collections.

---

# Research Context

This repository is an adaptation of a retrieval-augmented generation (RAG) pipeline developed during research conducted with the GIDS-AI Research Initiative (Jan 2026 – May 2026)!

The original research workflow involved:
- OCR preprocessing
- vector-based semantic retrieval
- structured prompt evaluation
- large-scale response generation across document collections

In order to protect currently unpublished research and private datasets, this repository uses a placeholder document and simplified demo prompts/questions while preserving the architecture of the pipeline.

---

# Features

- OpenAI vector store creation
- Automated grouped document uploads
- Semantic retrieval over document collections
- Structured prompt workflows
- Numerical response extraction from model outputs
- CSV result generation for future analysis

---

# Tech Stack

- Python
- OpenAI API
- OpenAI Vector Stores
- OpenAI File Search
- python-dotenv

---

# Repository Structure

```text
multisource-rag-research-pipeline/
├── ask.py
├── create_store.py
├── upload_docs.py
├── run_all.py
├── sample_questions.json
├── requirements.txt
├── .env.example
├── .gitignore
└── sample_docs/
    └── sample_author/
        └── sample_text.txt
```

---

# Pipeline Workflow

The workflow follows this architecture:

```text
Documents → Vector Store → Semantic Retrieval → Prompt Evaluation → Structured Outputs
```

1. Create a vector store
2. Upload document collections
3. Query retrieved context using structured prompts
4. Extract numerical responses
5. Save outputs to CSV

---

# Setup

## 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/multisource-rag-research-pipeline.git
cd multisource-rag-research-pipeline
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

---

# Usage

## Step 1: Create vector store

```bash
python3 create_store.py
```

---

## Step 2: Upload documents

```bash
python3 upload_docs.py
```

---

## Step 3: Run evaluation pipeline

```bash
python3 run_all.py
```

---

# Example Question Format

```json
[
  {
    "id": "Q1",
    "variable": "social_cooperation",
    "scale_type": "1-5",
    "question": "How strongly does the document describe cooperative social behavior among animals?",
    "coding": "1 = no cooperation described, 5 = extensive cooperation described"
  },
  {
    "id": "Q2",
    "variable": "protective_behavior",
    "scale_type": "1-5",
    "question": "To what extent does the document emphasize protection or caregiving toward younger animals?",
    "coding": "1 = no protective behavior described, 5 = heavily emphasized"
  }
]
```

---

# Example Pipeline Run

## Input Question

```text
How strongly does the document describe cooperative social behavior among animals?
```

---

## Retrieved Context

```text
Elephants display strong cooperative caregiving behaviors within family groups and coordinate movement across migration routes.
```

---

## Model Response

```text
4
```

---

# Example Output

```csv
survey,collection,model,question_id,raw_response,numeric_response
demo_survey,sample_author,gpt-4.1-mini,Q1,"4","4"
```

---