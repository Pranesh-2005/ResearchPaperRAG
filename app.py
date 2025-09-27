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