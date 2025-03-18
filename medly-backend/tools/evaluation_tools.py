from crewai import tool
from models.openai_wrapper import OpenAIWrapper
from integrations.rag_system import query_rag

class EvaluateEvidenceTool(tool):
    name = "Evaluate Evidence"
    description = "Evaluates the quality and relevance of evidence against research papers"

    def run(self, state):
        evidence_text = state.get("evidence_text", "")
        # Query RAG for context from research papers
        rag_results = query_rag(f"Evidence context: {evidence_text}")
        prompt = f"""
        Evidence: {evidence_text}
        Research from papers: {rag_results}
        Evaluate the quality and relevance of the provided evidence in the context of research papers.
        Provide a score (e.g., 1-10) and a summary explaining the assessment.
        """
        openai = OpenAIWrapper()
        return openai.get_completion(prompt)