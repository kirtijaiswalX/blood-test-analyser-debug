# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import traceback # For better error logging

from crewai import Crew, Process # MODIFIED: Removed Task, Agent as they are no longer defined here
from dotenv import load_dotenv
from langchain_community.chat_models import ChatLiteLLM

# Load environment variables from .env file
load_dotenv()

# --- Define your LLM instance here ---
llm = ChatLiteLLM(
    model="gemini-1.0-pro",
    temperature=0.5,
    litellm_api_key=os.getenv("GEMINI_API_KEY"), 
    vertex_ai_project=os.getenv("GCP_PROJECT_ID"),
    vertex_ai_location="us-central1", 
    verbose=True
)


# --- Import Agents from agents.py ---
from agents import doctor, verifier, nutritionist, exercise_specialist

# --- Import Tasks from tasks.py ---
from tasks import AnalysisTasks 
# Instantiate the tasks class
tasks = AnalysisTasks()


# --- FastAPI Application Setup ---
app = FastAPI(title="Blood Test Report Analyser")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file temporarily
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Default query if empty
        if not query or query.strip() == "":
            query = "Summarise my Blood Test Report"
            
    
        # Step 1: Doctor analyzes the report using the PDF tool
        doctor_analysis_task = tasks.analyze_report(agent=doctor, pdf_path=file_path)

        # Step 2: Verifier verifies the doctor's analysis.
        verifier_task = tasks.verify_analysis(agent=verifier, analysis_result_context=doctor_analysis_task)

        # Step 3: Nutritionist generates a plan based on doctor's analysis
        nutrition_task = tasks.generate_nutrition_plan(agent=nutritionist, blood_report_analysis_context=doctor_analysis_task)

        # Step 4: Exercise specialist generates a plan based on doctor's analysis
        exercise_task = tasks.generate_exercise_plan(agent=exercise_specialist, blood_report_analysis_context=doctor_analysis_task)

        medical_crew = Crew(
            agents=[doctor, verifier, nutritionist, exercise_specialist],
            tasks=[doctor_analysis_task, verifier_task, nutrition_task, exercise_task],
            process=Process.sequential,
            verbose=True,
            full_output=True
        )
        
        print(f"Starting Crew execution for query: '{query}' with file: {file.filename}")
        crew_result = medical_crew.kickoff(inputs={'query': query, 'file_path': file_path})
        
        print("\n--- Crew Execution Finished ---")
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(crew_result),
            "file_processed": file.filename
        }
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_e:
                print(f"Warning: Could not remove temporary file {file_path}: {cleanup_e}") 

# --- Entry point for Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)