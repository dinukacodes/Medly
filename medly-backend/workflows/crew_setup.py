# workflows/crew_setup.py
from crewai import Agent, Crew, Process, Task
from agents.data_processor import data_processor_agent
from agents.symptom_analyzer import symptom_analyzer_agent
from agents.urgency_router import urgency_router_agent
from agents.differential_generator import differential_generator_agent
from agents.certainty_evaluator import certainty_evaluator_agent
from agents.evidence_evaluator import evidence_evaluator_agent
from agents.specialty_router import specialty_router_agent
from agents.treatment_advisor import treatment_advisor_agent
from database.patient_history import get_patient_history
from workflows.diagnosis_process import create_diagnosis_tasks
from database.session_manager import get_session_state

def setup_crew():
    agents = {
        "data_processor": data_processor_agent,
        "symptom_analyzer": symptom_analyzer_agent,
        "urgency_router": urgency_router_agent,
        "differential_generator": differential_generator_agent,
        "certainty_evaluator": certainty_evaluator_agent,
        "evidence_evaluator": evidence_evaluator_agent,
        "specialty_router": specialty_router_agent,
        "treatment_advisor": treatment_advisor_agent
    }
    
    tasks = create_diagnosis_tasks(agents)
    
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    crew.get_patient_history = get_patient_history
    
    def custom_kickoff():
        state = get_session_state(crew.session_id)
        if not state:
            state = {
                "session_id": crew.session_id,
                "patient_data": crew.patient_data,
                "evidence": crew.evidence,
                "reasoning_steps": []
            }
        state["history"] = crew.get_patient_history(state["patient_data"]["name"])
        
        completed_steps = len(state.get("reasoning_steps", []))
        for task in tasks[completed_steps:]:
            task.execute(state)
            save_state_to_db(crew.session_id, state)
    
    crew.kickoff = custom_kickoff
    return crew