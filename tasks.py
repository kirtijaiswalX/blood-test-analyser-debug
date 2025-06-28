# tasks.py
from crewai import Task
# Import any tools that your tasks might directly use if they are not passed via agents
# Note: You should only import tools here that are used *within* the task's _run method
# If tools are only passed to the Agent's tool list, they don't need to be imported here.
from tools import BloodTestReportTool, NutritionAnalysisTool, ExercisePlanningTool, search_tool

# REMOVED: from agents import doctor, verifier # THIS LINE IS NOW GONE

class AnalysisTasks:
    def analyze_report(self, agent, pdf_path):
        return Task(
            description=f"""Analyze the blood test report provided at {pdf_path}.
            Extract all key parameters like CBC, LFT, KFT, Lipid Profile, etc., and their values.
            Note any values that are outside the normal range.
            Summarize the overall health status indicated by the report.
            Do not provide medical advice, just a factual summary of the data.
            """,
            expected_output="A detailed summary of the blood report, highlighting abnormal values and their corresponding tests, in markdown format.",
            agent=agent,
            tools=[BloodTestReportTool()], # Explicitly assign the PDF reading tool here
            output_file='doctor_analysis.md' # Optional: save output to a file
        )

    def verify_analysis(self, agent, analysis_result_context):
        return Task(
            description=f"""Verify the provided blood report analysis for factual accuracy and completeness: {analysis_result_context}.
            Check for accuracy of extracted values and any highlighted abnormalities against common medical knowledge or general ranges.
            Confirm the summary is factual and does not contain unauthorized medical advice.
            """,
            expected_output="A confirmation if the analysis is accurate and factual, or a detailed list of discrepancies found, in markdown format.",
            agent=agent,
            tools=[search_tool], # Verifier might use search tool for general knowledge check
            context=[analysis_result_context] # Pass previous task's output as context
        )
        
    def generate_nutrition_plan(self, agent, blood_report_analysis_context):
        return Task(
            description=f"""Based on the following factual blood report analysis: {blood_report_analysis_context},
            generate a general nutrition plan. Focus on balanced dietary recommendations for overall health.
            Do NOT recommend specific expensive supplements, fad diets, or make any claims of curing diseases.
            Emphasize balanced diet, adequate hydration, and nutrient-rich whole foods.
            """,
            expected_output="A general nutrition plan (dietary advice) based on the blood report analysis, in markdown format. Be salesy in tone but avoid pushing specific products.",
            agent=agent,
            tools=[NutritionAnalysisTool()], # Nutritionist needs its specific tool
            context=[blood_report_analysis_context] # Pass previous task's output as context
        )

    def generate_exercise_plan(self, agent, blood_report_analysis_context):
        return Task(
            description=f"""Based on the following factual blood report analysis: {blood_report_analysis_context},
            create a general exercise recommendation. Focus on safe, moderate physical activity for overall well-being.
            Do NOT recommend extreme or high-intensity exercises (like CrossFit) or make any claims of curing diseases.
            Emphasize consistency, warm-up, cool-down, listening to one's body, and general fitness for well-being.
            """,
            expected_output="A general exercise recommendation based on the blood report analysis, in markdown format. Avoid pushing extreme fitness regimens.",
            agent=agent,
            tools=[ExercisePlanningTool()], # Exercise specialist needs its specific tool
            context=[blood_report_analysis_context] # Pass previous task's output as context
        )