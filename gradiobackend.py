from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from gradio_client import Client, handle_file
import tempfile
import os
import uvicorn
from pydantic import BaseModel
from typing import List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Research Paper RAG API",
    description="FastAPI backend for Research Paper RAG using Gradio client",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    chat_history: Optional[List[Tuple[str, str]]] = []

class SessionInfo(BaseModel):
    session_id: str
    status: str

# Global client instance
gradio_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize Gradio client on startup"""
    global gradio_client
    try:
        gradio_client = Client("PraneshJs/ResearchPaperRAG")
        logger.info("Successfully connected to Gradio client")
    except Exception as e:
        logger.error(f"Failed to connect to Gradio client: {e}")
        # Don't raise exception to allow server to start

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Research Paper RAG API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    client_status = "connected" if gradio_client else "disconnected"
    return {
        "status": "healthy",
        "gradio_client": client_status,
        "message": "API is running"
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF file and get session ID"""
    global gradio_client
    
    if not gradio_client:
        raise HTTPException(status_code=503, detail="Gradio client not connected")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Use Gradio client to upload
        result = gradio_client.predict(
            pdf_file=handle_file(temp_file_path),
            api_name="/handle_upload"
        )
        
        # Clean up temp file
        os.unlink(temp_file_path)
        
        # Parse result
        session_info, chat_history = result
        
        # Extract session ID from the status message
        if "Session ID:" in session_info:
            session_id = session_info.split("Session ID: ")[1].strip()
        else:
            session_id = "unknown"
        
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "message": "PDF uploaded successfully",
            "chat_history": chat_history
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        # Clean up temp file if it exists
        try:
            os.unlink(temp_file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/ask")
async def ask_question(chat_data: ChatMessage):
    """Ask a question about the uploaded paper"""
    global gradio_client
    
    if not gradio_client:
        raise HTTPException(status_code=503, detail="Gradio client not connected")
    
    if not chat_data.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Use Gradio client to ask question
        result = gradio_client.predict(
            message=chat_data.message,
            chat_history=chat_data.chat_history,
            api_name="/handle_question"
        )
        
        # Parse result
        updated_chat_history, _ = result
        
        return JSONResponse({
            "success": True,
            "chat_history": updated_chat_history,
            "message": "Question processed successfully"
        })
        
    except Exception as e:
        logger.error(f"Question error: {e}")
        raise HTTPException(status_code=500, detail=f"Question processing failed: {str(e)}")

@app.post("/clear")
async def clear_chat():
    """Clear the chat history"""
    global gradio_client
    
    if not gradio_client:
        raise HTTPException(status_code=503, detail="Gradio client not connected")
    
    try:
        result = gradio_client.predict(api_name="/clear_chat")
        
        return JSONResponse({
            "success": True,
            "chat_history": [],
            "message": "Chat cleared successfully"
        })
        
    except Exception as e:
        logger.error(f"Clear chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Clear chat failed: {str(e)}")

@app.get("/status")
async def get_status():
    """Get API status"""
    return {
        "api_status": "running",
        "gradio_client_status": "connected" if gradio_client else "disconnected"
    }

if __name__ == "__main__":
    # Render port detection
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "gradiobackend:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Set to False for production
        log_level="info"
    )