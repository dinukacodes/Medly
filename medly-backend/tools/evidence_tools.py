from crewai import tool
from integrations.pdf_processor import extract_text_from_pdf

class ProcessEvidenceTool(tool):
    name = "Process Evidence"
    description = "Extracts text from uploaded evidence files"
    
    def run(self, state):
        file_ids = state.get("evidence", [])
        evidence_text = []
        for file_id in file_ids:
            file_path = f"uploads/{file_id}.pdf"
            text = extract_text_from_pdf(file_path)
            evidence_text.append(text)
        return "\n".join(evidence_text) if evidence_text else "No evidence text available" 
