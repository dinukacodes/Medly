# from fastapi import APIRouter, BackgroundTasks
# from pydantic import BaseModel
# from workflows.crew_setup import crew
# from database.session_manager import save_patient_data
# import uuid

# router = APIRouter()

# class PatientData(BaseModel):
#     name: str
#     age: int
#     gender: str
#     symptoms: list[str]
#     medications: list[str]

# class DiagnosisRequest(BaseModel):
#     model: str
#     patient: PatientData
#     evidence: list[str] = []

# @router.post("/start-diagnosis")
# async def start_diagnosis(request: DiagnosisRequest, background_tasks: BackgroundTasks):
#     session_id = str(uuid.uuid4())
#     save_patient_data(request.patient.dict(), session_id)
#     crew.session_id = session_id
#     crew.patient_data = request.patient.dict()
#     crew.evidence = request.evidence
#     background_tasks.add_task(crew.kickoff)
#     return {"session_id": session_id, "status": "started"}
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from workflows.crew_setup import setup_crew
from database.session_manager import save_patient_data
import uuid

router = APIRouter()

class PatientData(BaseModel):
    name: str
    age: int
    gender: str
    symptoms: list[str]
    medications: list[str]

class DiagnosisRequest(BaseModel):
    model: str
    patient: PatientData
    evidence: list[str] = []

@router.post("/start-diagnosis")
async def start_diagnosis(request: DiagnosisRequest, background_tasks: BackgroundTasks):
    session_id = str(uuid.uuid4())
    save_patient_data(request.patient.dict(), session_id)
    
    # Create a new crew instance for this diagnosis
    crew = setup_crew()
    crew.session_id = session_id
    crew.patient_data = request.patient.dict()
    crew.evidence = request.evidence
    
    # Start the diagnosis process in the background
    background_tasks.add_task(crew.kickoff)
    
    return {"session_id": session_id, "status": "started"} 