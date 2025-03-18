from crewai import Agent
from tools.evaluation_tools import EvaluateCertaintyTool

certainty_evaluator_agent = Agent(
    role="Certainty Evaluator",
    goal="Evaluate the certainty of the generated diagnoses",
    tools=[EvaluateCertaintyTool()],
    llm="gpt-4o",
    verbose=True
) 
