from crewai import Agent
from tools.symptom_tools import AnalyzeSymptomsTool

symptom_analyzer_agent = Agent(
    role="Symptom Analyzer",
    goal="Analyze patient symptoms to identify patterns and possible conditions",
    tools=[AnalyzeSymptomsTool()],
    llm="gpt-4o",
    verbose=True
) 
