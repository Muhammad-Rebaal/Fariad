import os
import shutil
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from typing import Optional
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import groq

from fastapi.middleware.cors import CORSMiddleware

# Import the refactored automation script
from main import run_automation
from database import init_db, get_or_create_user, create_complaint, get_similar_complaints_count, get_cached_response, save_cached_response

app = FastAPI(title="Gemini Automation API")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("groq_api")
APP_PASSWORD = os.getenv("App_password")
SENDER_EMAIL = "mrebaal14@gmail.com"

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

@app.post("/launch-complaint")
def launch_complaint(
    name: str = Form(...),
    email: str = Form(...),
    district: str = Form(...),
    postal_code: str = Form(...),
    street: str = Form(...),
    prompt: str = Form(...),
    response: str = Form(...)
):
    try:
        if not GROQ_API_KEY:
            raise ValueError("Groq API key not found in .env")
        if not APP_PASSWORD:
            raise ValueError("App password not found in .env")

        # 1. Generate Formal Application via Groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        
        system_prompt = "You are a professional legal assistant. Write a formal complaint letter or application to the relevant municipal authority on behalf of the citizen. Keep it professional, concise, and structured."
        user_prompt = f"Name: {name}\nEmail: {email}\nAddress: {street}, {district}, {postal_code}\n\nUser Issue: {prompt}\n\nAuthority Advice (from Gemini): {response}\n\nPlease generate the formal application letter based on this information."
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-120b",
            temperature=0.7,
        )
        
        application_letter = chat_completion.choices[0].message.content
        
        # 2. Send Email via SMTP
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = f"Formal Complaint Application - {district}"
        
        body = f"Hello {name},\n\nAs requested, here is the generated formal application for your complaint. You can forward this to the respective authorities.\n\n------------------------\n\n{application_letter}\n\n------------------------\n\nPowered by Fariad."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Note: Depending on the email service, app passwords might require removing spaces
        clean_password = APP_PASSWORD.replace(" ", "").replace('"', '') 
        server.login(SENDER_EMAIL, clean_password)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, email, text)
        server.quit()

        return JSONResponse(content={"status": "success", "message": "Formal complaint letter has been generated and emailed to you successfully!"})
        
    except Exception as e:
        print(f"Error launching complaint: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# Serve the static frontend files
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    init_db()
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
