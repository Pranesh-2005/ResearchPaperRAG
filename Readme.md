# 📄 ResearchPaperRAG

**ResearchPaperRAG** is a cutting-edge tool designed to help you analyze and interact with research papers using Retrieval-Augmented Generation (RAG). By leveraging state-of-the-art language models and vector search, it allows users to upload PDFs and ask questions, receiving insightful answers in real-time. With a modern web interface and backend powered by OpenRouter.ai and HuggingFace, ResearchPaperRAG streamlines research workflows for academics, students, and enthusiasts.

---

## 🚀 Features

- **PDF Upload & Parsing:** Seamlessly upload research papers in PDF format.
- **Retrieval-Augmented Generation:** Ask questions and get context-aware answers sourced directly from your paper.
- **Chat-like Interface:** Intuitive frontend that feels like chatting with your research assistant.
- **State-of-the-Art Embeddings:** Uses powerful language models via HuggingFace for document understanding.
- **Fast Vector Search:** Efficient document chunking and retrieval using FAISS.
- **Cross-Platform Frontend:** Responsive web app with PWA support for desktop & mobile.
- **Easy Backend Setup:** Gradio and Flask backend, with API integration for OpenRouter.ai.
- **Secure API Key Management:** Environment variable support for sensitive credentials.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js & npm (for frontend development)
- [OpenRouter.ai API Key](https://openrouter.ai/)
- [HuggingFace account](https://huggingface.co/) (optional, for advanced features)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ResearchPaperRAG.git
cd ResearchPaperRAG
```

### 2. Backend Setup

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your-OpenRouter.ai-api-key
```

Start the backend:

```bash
python gradiobackend.py
# Or, if using app.py:
python app.py
```

### 3. Frontend Setup

```bash
cd frontend
npm install           # If using build tools
# Or simply open index.html in your browser for basic usage
```

---

## 💡 Usage

1. **Start the Backend:**  
   Run `python gradiobackend.py` or `python app.py` to start the API server.

2. **Open the Frontend:**  
   Open `frontend/index.html` in your browser, or deploy the frontend as a static site.

3. **Upload a PDF:**  
   Use the interface to upload your research paper.

4. **Ask Questions:**  
   Type your queries into the chat and receive answers sourced from your document!

5. **API Usage:**  
   You can also interact directly with the API for custom workflows.

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. **Fork the repository**
2. **Create a new branch:**  
   `git checkout -b feature/your-feature`
3. **Commit your changes**
4. **Push your branch:**  
   `git push origin feature/your-feature`
5. **Open a Pull Request**

**Issues and suggestions** can be posted in the [GitHub Issues](https://github.com/yourusername/ResearchPaperRAG/issues) section.

---

## 📄 License

This project is licensed under the **MIT License**.  
See [LICENSE](LICENSE) for more details.

---

> **Made with ❤️ for researchers, students, and curious minds everywhere.**

---

## 📁 Project Structure

```
ResearchPaperRAG/
├── .env.example
├── app.py
├── gradiobackend.py
├── frontend/
│   ├── index.html
│   ├── manifest.json
│   ├── script.js
│   ├── style.css
└── README.md
```

---

## 📬 Contact

For questions or support, reach out via [GitHub Issues](https://github.com/yourusername/ResearchPaperRAG/issues).

---

Happy researching! 🚀

## License
This project is licensed under the **MIT** License.

---
🔗 GitHub Repo: https://github.com/Pranesh-2005/ResearchPaperRAG