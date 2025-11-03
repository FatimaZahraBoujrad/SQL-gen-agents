import os
import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get project root from environment
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
if not PROJECT_ROOT:
    raise ValueError("PROJECT_ROOT not set in environment variables")

# --- 1️⃣ Load embedding model ---
print(" Loading embedding model...")
embedder = SentenceTransformer(
    os.path.join(PROJECT_ROOT, "chatbot_agent/chtabot_agent/rag/model/all-MiniLM-L6-v2-local")
)

# --- 2️⃣ Chroma store at project root ---
CHROMA_DIR = os.path.join(PROJECT_ROOT, "chroma_store")
client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_or_create_collection(name="kpi_docs")

# --- 3️⃣ Load KPI JSON files ---
kpi_folder = os.path.join(PROJECT_ROOT, "full_scrapper/kpis_extracted")

def load_all_kpi_files(folder_path):
    kpis = []
    for filename in os.listdir(folder_path):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            clean_name = os.path.splitext(filename)[0]
            parts = clean_name.split("_")
            report_name = " ".join(parts[:-1])
            for kpi in data:
                kpi["report_name"] = report_name
                kpis.append(kpi)
    return kpis

kpi_docs = load_all_kpi_files(kpi_folder)

# --- 4️⃣ Prepare and embed ---
documents = []
metadatas = []
ids = []

def format_kpi_text(kpi: dict) -> str:
    return f"KPI Name: {kpi['name']}\nKPI Value: {kpi['value']}\nReport: {kpi['report_name']}\n"

for kpi in kpi_docs:
    documents.append(format_kpi_text(kpi))
    metadatas.append({
        "doc_type": "extracted_kpi",
        "report": kpi["report_name"],
        "kpi_name": kpi["name"]
    })
    ids.append(str(uuid4()))

print(" Embedding and inserting into Chroma...")
embeddings = embedder.encode(documents).tolist()
collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
print(" Done! Embedded", len(documents), "KPIs.")
