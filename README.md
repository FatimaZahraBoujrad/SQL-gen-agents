
***

# Multi-Agent SQL Query Generator with RAG System

This project implements a multi-agent system designed to generate SQL queries from natural language prompts using Retrieval-Augmented Generation (RAG) techniques. The system integrates large language model(s) with vector-based retrieval for improved accuracy and grounded query generation.

## Key Features

- **Multi-Agent Architecture:** Modular agents handle different responsibilities including chat interaction, logic processing, SQL generation, and validation.
- **Large Language Model:** Uses LLaMA as the foundational language model for natural language understanding and SQL generation.
- **Retrieval-Augmented Generation (RAG):** Implements retrieve and embed workflow for enhanced retrieval of relevant context:
  - Embedding generation and vector storage with ChromaDB.
  - Efficient retrieval of relevant data to inform query generation.
- **API Backend:** FastAPI-based API for serving requests, orchestrating calls between agents, and managing workflows.

## Components

- **Agents:**
  - `chat_agent.py`: Manages conversational interactions.
  - `logic_agent.py`: Processes logical reasoning and task coordination.
  - `sql_gen_agent.py`: Generates SQL queries from interpreted prompts.
  - `sql_validator.py`: Validates generated SQL queries for correctness.
  - `response_agent.py`: Constructs final responses combining generated SQL and additional information.
  
- **API:**
  - Contains orchestration logic using FastAPI in `orchestration.py`.
  - Exposes endpoints to interact with the multi-agent system.
  
- **RAG System:**
  - Embedding generation and vector storage performed with ChromaDB.
  - Implements retrieval of relevant information to augment prompts for improved query generation.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the FastAPI server to start the API:

```bash
uvicorn api.orchestration:app --reload
```

Then send requests with natural language prompts to the API endpoint to receive generated SQL queries.

## Technologies Used

- Python
- LLaMA Large Language Model
- ChromaDB vector store
- FastAPI for API management
- Retrieval-Augmented Generation (RAG) techniques



***

