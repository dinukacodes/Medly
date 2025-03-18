from crewai import   tool
from models.openai_wrapper import OpenAIWrapper

class RecommendTreatmentTool(tool):
    name = "Recommend Treatment"
    description = "Recommends treatments based on diagnosis"
    
    def run(self, state):
        diagnosis = state["diagnosis"]
        patient_data = state["patient_data"]
        prompt = f"Diagnosis: {diagnosis}\nPatient: {patient_data}\nRecommend evidence-based treatments."
        openai = OpenAIWrapper()
        return openai.get_completion(prompt)