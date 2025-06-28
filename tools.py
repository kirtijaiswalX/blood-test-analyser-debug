# tools.py
import os
from dotenv import load_dotenv
load_dotenv()

# Import BaseTool from crewai itself
from crewai.tools import BaseTool

# Import PDF loader from Langchain Community
from langchain_community.document_loaders import PyPDFLoader

# For Serper search, import GoogleSerperAPIWrapper from its specific submodule
# THIS IS THE LINE THAT NEEDS TO BE CORRECTED:
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper # <--- THIS IS THE CORRECT IMPORT


## Creating search tool
class CustomSerperSearchTool(BaseTool):
    name: str = "Serper Search Tool"
    description: str = "Performs a Google search using Serper API to find relevant information."

    def _run(self, query: str) -> str:
        # Instantiate GoogleSerperAPIWrapper
        serper_wrapper = GoogleSerperAPIWrapper() # Use the correctly imported class name
        return serper_wrapper.run(query)

search_tool = CustomSerperSearchTool()


## Creating custom pdf reader tool
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Reads and extracts text content from blood test report PDFs given a file path."

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: File not found at {file_path}")
        
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            full_report = "\n".join([page.page_content for page in pages])
            
            # Simple whitespace cleanup
            full_report = ' '.join(full_report.split())
            
            return full_report
        except Exception as e:
            raise RuntimeError(f"Error reading PDF file {file_path}: {str(e)}")


## Creating Nutrition Analysis Tool
class NutritionAnalysisTool(BaseTool):
    name: str = "Nutrition Analysis Tool"
    description: str = "Analyzes processed blood report data for nutrition insights."

    def _run(self, blood_report_data: str) -> str:
        processed_data = ' '.join(blood_report_data.split())
        
        # TODO: Implement nutrition analysis logic here
        return f"Nutrition analysis functionality to be implemented for: {processed_data[:200]}..."


## Creating Exercise Planning Tool
class ExercisePlanningTool(BaseTool):
    name: str = "Exercise Planning Tool"
    description: str = "Creates an exercise plan based on blood report data."

    def _run(self, blood_report_data: str) -> str:
        # TODO: Implement exercise planning logic here
        return f"Exercise planning functionality to be implemented for: {blood_report_data[:200]}..."