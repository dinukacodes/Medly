from crewai import Agent
from tools.evidence_tools import ProcessEvidenceTool

data_processor_agent = Agent(
    role="Data Processor",
    goal="Process uploaded evidence files into usable text",
    tools=[ProcessEvidenceTool()],
    llm="gpt-4o",
    verbose=True
) 
