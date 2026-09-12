import os
import shutil
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from typing import Optional
import hashlib

from fastapi.middleware.cors import CORSMiddleware

# Import the refactored automation script
from main import run_automation
from database import init_db, get_or_create_user, create_complaint, get_similar_complaints_count, get_cached_response, save_cached_response

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
    image: Optional[UploadFile] = File(None),
    name: str = Form(""),
    email: str = Form(""),
    district: str = Form(""),
    postal_code: str = Form(""),
    street: str = Form("")
):
    image_path = None
    image_hash = None
    
    if image and image.filename:
        # Save the uploaded image temporarily
        image_path = os.path.join(IMG_DIR, image.filename)
        
        # Read the file content and compute SHA-256 hash
        file_content = image.file.read()
        image_hash = hashlib.sha256(file_content).hexdigest()
        
        with open(image_path, "wb") as buffer:
            buffer.write(file_content)
            
    try:
        # Save user to DB
        user_id = None
        user_data = {
            "name": name,
            "email": email,
            "district": district,
            "postal_code": postal_code,
            "street": street
        }
        if email:
            user_id = get_or_create_user(name, email, district, postal_code, street)
            prior_count = get_similar_complaints_count(district, street)
            create_complaint(user_id, prompt)
            print(f"Saved user {email} (ID: {user_id}) to database.")
            user_data["prior_complaints"] = prior_count
            
        # Check cache
        if image_hash:
            cached_res = get_cached_response(image_hash)
            if cached_res:
                print("Found cached response for this image! Skipping automation and returning cached result.")
                return JSONResponse(content={"status": "success", "response": cached_res})
            
        # Run the automation script
        print(f"Running automation with prompt: '{prompt}' and image: {image_path}")
        result_text = run_automation(prompt_text=prompt, image_path=image_path, user_data=user_data)
        
        # Save to cache for future identical images
        if image_hash and not result_text.startswith("Error:"):
            save_cached_response(image_hash, result_text)
            
        return JSONResponse(content={"status": "success", "response": result_text})
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# Serve the static frontend files
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    init_db()
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
