# 📄 ResearchPaperRAG

**ResearchPaperRAG** is a cutting-edge tool designed to help you analyze and interact with research papers using Retrieval-Augmented Generation (RAG). By leveraging state-of-the-art language models and vector search, it allows users to upload PDFs and ask questions, receiving insightful, context-aware answers.

---

## ✨ Features

- **PDF Upload**: Seamlessly upload and process research papers in PDF format.
- **Retrieval-Augmented Generation**: Combines retrieval of relevant paper sections with generative AI for precise answers.
- **Fast & Accurate**: Utilizes FAISS for high-speed vector search and HuggingFace embeddings for semantic understanding.
- **User-friendly Interface**: Simple UI with [Gradio](https://gradio.app/) for easy interaction.
- **Secure API Integration**: Connects to OpenRouter.ai for model inference using your API key.

---

## ⚡ Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/ResearchPaperRAG.git
    cd ResearchPaperRAG
    ```

2. **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your environment variables**
    - Copy `.env.example` to `.env` and add your [OpenRouter.ai](https://openrouter.ai/) API key:
      ```
      OPENROUTER_API_KEY=<your-OpenRouter.ai-api-key>
      ```

---

## 🚀 Usage

1. **Run the app**
    ```bash
    python app.py
    ```

2. **Open your browser**
    - Access the Gradio interface at the displayed URL.

3. **Upload a research paper**
    - Click "Upload" and select your PDF.

4. **Ask questions**
    - Type your question about the paper and get context-aware responses!

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes.
4. Push to your branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

> Made with ❤️ for researchers and AI enthusiasts!

## License
This project is licensed under the **MIT** License.

---
🔗 GitHub Repo: https://github.com/Pranesh-2005/ResearchPaperRAG