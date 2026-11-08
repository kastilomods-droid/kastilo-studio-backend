from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile

app = FastAPI(title="KASTILO STUDIO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "project": "KASTILO STUDIO",
        "status": "online",
        "message": "KASTILO STUDIO backend is ready"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    allowed = [".wav", ".mp3", ".m4a", ".ogg", ".flac"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        return JSONResponse(
            status_code=400,
            content={"error": "Unsupported audio format"}
        )

    data = await file.read()

    if len(data) > 25 * 1024 * 1024:
        return JSONResponse(
            status_code=413,
            content={"error": "Maximum file size is 25 MB"}
        )

    return {
        "filename": file.filename,
        "size_bytes": len(data),
        "status": "uploaded",
        "message": "Audio received successfully"
    }
