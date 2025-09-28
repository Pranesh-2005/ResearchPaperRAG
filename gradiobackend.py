from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
import tempfile, os

app = Flask(__name__)
CORS(app)

# Connect to HuggingFace Space
gradio_client = Client("PraneshJs/ResearchPaperRAG")

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "running", "service": "ResearchPaperRAG"})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            file.save(temp_file)
            temp_file_path = temp_file.name

        result = gradio_client.predict(
            pdf_file=handle_file(temp_file_path),
            api_name="/handle_upload"
        )
        os.unlink(temp_file_path)

        # HuggingFace Space returns: (session_id, chat_history)
        session_id, chat_history = result
        return jsonify({"session_id": session_id, "chat_history": chat_history})

    except Exception as e:
        return jsonify({"error": f"Upload failed: {e}"}), 500

@app.route("/ask", methods=["POST"])
def ask_question():
    # Accept both JSON body and query params
    if request.is_json:
        data = request.get_json()
        message = data.get("message", "")
        chat_history = data.get("chat_history", [])
    else:
        message = request.args.get("message", "")
        chat_history = []

    # Ensure chat_history is valid
    formatted_history = []
    for item in chat_history:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            formatted_history.append(tuple(item))

    try:
        result = gradio_client.predict(
            message=message,
            chat_history=tuple(formatted_history),
            api_name="/handle_question"   # This is the correct API
        )
        updated_chat, reply = result
        return jsonify({"chat_history": updated_chat, "reply": reply})
    except Exception as e:
        return jsonify({"error": f"Question failed: {e}"}), 500

@app.route("/clear", methods=["POST"])
def clear_chat():
    try:
        result = gradio_client.predict(api_name="/clear_chat")
        return jsonify({"chat_history": result})
    except Exception as e:
        return jsonify({"error": f"Clear failed: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
