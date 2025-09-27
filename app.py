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