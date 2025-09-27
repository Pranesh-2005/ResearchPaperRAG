import os
import time
import shutil
import uuid
import gradio as gr
import requests
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
STORAGE_DIR = "storage"
CLEANUP_INTERVAL = 600  # 10 min
SESSION_TTL = 1000      # 30 min
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "z-ai/glm-4.5-air:free"

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# === CLEANUP THREAD ===
def cleanup_old_sessions():
    while True:
        now = time.time()
        for folder in os.listdir(STORAGE_DIR):
            path = os.path.join(STORAGE_DIR, folder)
            if os.path.isdir(path) and now - os.path.getmtime(path) > SESSION_TTL:
                shutil.rmtree(path)
        time.sleep(CLEANUP_INTERVAL)

Thread(target=cleanup_old_sessions, daemon=True).start()

# === PDF PROCESSING ===
def process_pdf(pdf_file):
    if pdf_file is None:
        return "No file uploaded.", "", []

    session_id = str(uuid.uuid4())
    reader = PdfReader(pdf_file.name)
    text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    session_path = os.path.join(STORAGE_DIR, session_id)
    os.makedirs(session_path, exist_ok=True)

    db = FAISS.from_texts(chunks, embeddings)
    db.save_local(session_path)

    chat_history = [("System", "Paper uploaded and processed. You can now ask questions.")]
    return f"Paper uploaded successfully. Session ID: {session_id}", session_id, chat_history

# === QUERY FUNCTION ===
def query_paper(session_id, user_message, chat_history):
    if not session_id or not os.path.exists(os.path.join(STORAGE_DIR, session_id)):
        chat_history = chat_history or []
        chat_history.append(("System", "Session expired or not found. Upload the paper again."))
        return chat_history, ""

    if not user_message.strip():
        return chat_history, ""

    session_path = os.path.join(STORAGE_DIR, session_id)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(session_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Use invoke() instead of deprecated method
    docs = retriever.invoke(user_message)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    You are an AI assistant. Explain the following research paper content in simple terms and answer the question.
    Use your own knowledge also and make it more technical but simpler explanation should be like professor with 
    high knowledge but teaches in awesome way with more technical stuff but easier.
    Context from paper:
    {context}
    Question: {user_message}
    Answer:
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful research paper explainer. Explain all concepts clearly with technical aspects but in an easy way."
            },
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=payload)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"].strip()
        else:
            answer = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        answer = f"Error: {str(e)}"

    # Update chat history (tuple format)
    chat_history = chat_history or []
    chat_history.append((user_message, answer))

    return chat_history, ""
