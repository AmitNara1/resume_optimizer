from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Resume Optimizer API running"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        # Extract text from PDF
        if file.filename and file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = content.decode('utf-8')
        
        # Simple analysis
        keywords = ['Python', 'Java', 'AWS', 'SQL', 'Docker', 'AI', 'ML', 'React']
        found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
        missing_keywords = [kw for kw in keywords if kw.lower() not in text.lower()]
        
        score = len(found_keywords) * 10
        
        feedback = {
            "suggestions": f"Found skills: {', '.join(found_keywords)}. Consider adding: {', '.join(missing_keywords[:3])}",
            "score": min(score, 100),
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords
        }
        
        return feedback
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)