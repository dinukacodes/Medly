from crewai import Agent
from tools.evaluation_tools import EvaluateEvidenceTool
from utils.exceptions import InsufficientDataError

evidence_evaluator_agent = Agent(
    role="Evidence Evaluator",
    goal="Evaluate the quality and relevance of uploaded evidence against research papers",
    tools=[EvaluateEvidenceTool()],
    llm="gpt-4o",
    verbose=True,
    callback=lambda state: check_data_sufficiency(state, "Evidence Evaluator")
)

def check_data_sufficiency(state, role):
    evidence_text = state.get("evidence_text", "")
    if not evidence_text:
        raise InsufficientDataError("No evidence text available. Please upload medical evidence.", role)
    return state