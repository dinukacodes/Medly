from crewai import tool
from models.openai_wrapper import OpenAIWrapper

class ClassifyUrgencyTool(tool):
    name = "Classify Urgency"
    description = "Classifies the urgency of the patient's condition"
    
    def run(self, state):
        symptom_analysis = state["symptom_analysis"]
        prompt = f"Given symptom analysis: {symptom_analysis}, classify urgency (Low, Medium, High)."
        openai = OpenAIWrapper()
        return openai.get_completion(prompt)

class GenerateDifferentialTool(tool):
    name = "Generate Differential"
    description = "Generates a list of differential diagnoses using symptom analysis, evidence, and research papers"

    def run(self, state):
        symptom_analysis = state["symptom_analysis"]
        evidence_text = state.get("evidence_text", "")
        # Query RAG for relevant research
        rag_results = query_rag(f"Symptoms: {symptom_analysis}")
        prompt = f"""
        Symptom analysis: {symptom_analysis}
        Evidence: {evidence_text}
        Research from papers: {rag_results}
        Generate a list of differential diagnoses based on the symptom analysis, evidence, and relevant research.
        """
        openai = OpenAIWrapper()
        return openai.get_completion(prompt)

class RouteSpecialtyTool(tool):
    name = "Route Specialty"
    description = "Routes the case to the appropriate specialty"
    
    def run(self, state):
        differential = state["differential"]
        prompt = f"Given differential diagnoses: {differential}, recommend the appropriate medical specialty."
        openai = OpenAIWrapper()
        return openai.get_completion(prompt)