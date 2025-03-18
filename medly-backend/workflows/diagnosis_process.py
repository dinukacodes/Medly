# workflows/diagnosis_process.py
from crewai import Task
from database.session_manager import save_state_to_db
from datetime import datetime
from utils.exceptions import InsufficientDataError

def create_diagnosis_tasks(agents):
    tasks = []

    def handle_task_execution(agent, description, expected_output, state):
        try:
            result = agent.tools[0].run(state)
            state["reasoning_steps"].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"{description}: {result}"
            })
            return result
        except InsufficientDataError as e:
            state["reasoning_steps"].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"Insufficient data detected by {e.agent_role}: {e.message}"
            })
            state["status"] = "awaiting_user_input"
            state["user_request"] = e.message
            save_state_to_db(state["session_id"], state)
            raise

    # Step 1: Process Evidence
    tasks.append(Task(
        description="Process and extract text from uploaded evidence files",
        agent=agents["data_processor"],
        expected_output="Processed evidence text",
        callback=lambda state: {"evidence_text": handle_task_execution(agents["data_processor"], "Evidence processed", "Processed evidence text", state)}
    ))

    # Step 2: Analyze Symptoms
    tasks.append(Task(
        description="Analyze patient symptoms using Chain-of-Thought reasoning",
        agent=agents["symptom_analyzer"],
        expected_output="Structured symptom analysis",
        callback=lambda state: {"symptom_analysis": handle_task_execution(agents["symptom_analyzer"], "Symptom analysis", "Structured symptom analysis", state)}
    ))

    # Step 3: Evaluate Evidence (Now with RAG)
    tasks.append(Task(
        description="Evaluate the quality and relevance of evidence against research papers",
        agent=agents["evidence_evaluator"],
        expected_output="Evidence evaluation score and summary",
        callback=lambda state: {"evidence_evaluation": handle_task_execution(agents["evidence_evaluator"], "Evidence evaluation", "Evidence evaluation score and summary", state)}
    ))

    # Step 4: Classify Urgency
    tasks.append(Task(
        description="Classify the urgency of the patient's condition",
        agent=agents["urgency_router"],
        expected_output="Urgency classification (Low, Medium, High)",
        callback=lambda state: {"urgency": handle_task_execution(agents["urgency_router"], "Urgency classified", "Urgency classification", state)}
    ))

    # Step 5: Generate Differential (Now with RAG)
    tasks.append(Task(
        description="Generate a list of possible differential diagnoses using symptom analysis, evidence, and research papers",
        agent=agents["differential_generator"],
        expected_output="List of differential diagnoses",
        callback=lambda state: {"differential": handle_task_execution(agents["differential_generator"], "Differential diagnoses", "List of differential diagnoses", state)}
    ))

    # Step 6: Evaluate Certainty
    tasks.append(Task(
        description="Evaluate the certainty of the generated diagnoses",
        agent=agents["certainty_evaluator"],
        expected_output="Diagnostic certainty evaluation",
        callback=lambda state: {"certainty": handle_task_execution(agents["certainty_evaluator"], "Certainty evaluation", "Diagnostic certainty evaluation", state)}
    ))

    # Step 7: Route Specialty
    tasks.append(Task(
        description="Route the case to the appropriate medical specialty",
        agent=agents["specialty_router"],
        expected_output="Recommended medical specialty",
        callback=lambda state: {"specialty": handle_task_execution(agents["specialty_router"], "Specialty routed", "Recommended medical specialty", state)}
    ))

    # Step 8: Recommend Treatment (Now with RAG)
    tasks.append(Task(
        description="Recommend treatments based on diagnosis, patient data, and research papers",
        agent=agents["treatment_advisor"],
        expected_output="Treatment recommendations",
        callback=lambda state: {"diagnosis": {"differential": state["differential"], "certainty": state["certainty"], "treatment": handle_task_execution(agents["treatment_advisor"], "Treatment recommended", "Treatment recommendations", state)}}
    ))

    return tasks