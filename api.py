import os
import shutil
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

# Import the refactored automation script
from main import run_automation

app = FastAPI(title="Gemini Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure directories exist
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

@app.post("/ask")
def ask_gemini(
    prompt: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    image_path = None
    
    if image and image.filename:
        # Save the uploaded image temporarily
        image_path = os.path.join(IMG_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
    try:
        # Run the automation script
        print(f"Running automation with prompt: '{prompt}' and image: {image_path}")
        result_text = run_automation(prompt_text=prompt, image_path=image_path)
        
        return JSONResponse(content={"status": "success", "response": result_text})
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# Serve the static frontend files
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
