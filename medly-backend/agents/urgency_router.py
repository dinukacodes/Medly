from crewai import Agent
from tools.diagnostic_tools import ClassifyUrgencyTool

urgency_router_agent = Agent(
    role="Urgency Router",
    goal="Classify the urgency of the patient's condition",
    tools=[ClassifyUrgencyTool()],
    llm="gpt-4o",
    verbose=True
) 
