from fastapi import APIRouter, UploadFile, File
from utils.file_utils import save_uploaded_file
from integrations.pdf_processor import extract_text_from_pdf
import uuid

router = APIRouter()

@router.post("/upload-evidence")
async def upload_evidence(files: list[UploadFile] = File(...)):
    file_ids = []
    for file in files:
        file_id = str(uuid.uuid4())
        file_path = save_uploaded_file(file, file_id)
        text = extract_text_from_pdf(file_path)
        # Optionally save text to database
        file_ids.append(file_id)
    return {"file_ids": file_ids, "status": "uploaded"}