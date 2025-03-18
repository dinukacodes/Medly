from crewai import Agent
from tools.diagnostic_tools import RouteSpecialtyTool

specialty_router_agent = Agent(
    role="Specialty Router",
    goal="Route the case to the appropriate medical specialty",
    tools=[RouteSpecialtyTool()],
    llm="gpt-4o",
    verbose=True
) 
