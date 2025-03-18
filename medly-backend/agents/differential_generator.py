from crewai import Agent
from tools.diagnostic_tools import GenerateDifferentialTool
from utils.exceptions import InsufficientDataError

differential_generator_agent = Agent(
    role="Differential Generator",
    goal="Generate a list of possible differential diagnoses using symptom analysis, evidence, and research papers",
    tools=[GenerateDifferentialTool()],
    llm="gpt-4o",
    verbose=True,
    callback=lambda state: check_data_sufficiency(state, "Differential Generator")
)

def check_data_sufficiency(state, role):
    symptom_analysis = state.get("symptom_analysis", "")
    evidence_text = state.get("evidence_text", "")
    if not symptom_analysis:
        raise InsufficientDataError("Symptom analysis missing. Please ensure symptoms are analyzed first.", role)
    if not evidence_text:
        raise InsufficientDataError("No evidence text available. Please upload additional medical evidence.", role)
    return state