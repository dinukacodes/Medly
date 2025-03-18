from crewai import Agent
from tools.treatment_tools import RecommendTreatmentTool
from utils.exceptions import InsufficientDataError

treatment_advisor_agent = Agent(
    role="Treatment Advisor",
    goal="Recommend treatments based on diagnosis, patient data, and research papers",
    tools=[RecommendTreatmentTool()],
    llm="gpt-4o",
    verbose=True,
    callback=lambda state: check_data_sufficiency(state, "Treatment Advisor")
)

def check_data_sufficiency(state, role):
    diagnosis = state.get("diagnosis", {})
    patient_data = state.get("patient_data", {})
    if not diagnosis.get("differential"):
        raise InsufficientDataError("No differential diagnoses available. Please complete diagnosis first.", role)
    if not patient_data:
        raise InsufficientDataError("No patient data provided. Please submit patient details.", role)
    return state