from crewai import Tool
from models.openai_wrapper import OpenAIWrapper

class AnalyzeSymptomsTool(Tool):
    name = "Analyze Symptoms"
    description = "Analyzes patient symptoms using Chain-of-Thought reasoning with few-shot examples"

    def run(self, state):
        patient_data = state["patient_data"]
        history = state.get("history", [])
        # Construct a detailed prompt with few-shot examples
        prompt = f"""
        You are an expert medical symptom analyzer. Your task is to analyze patient symptoms using Chain-of-Thought reasoning:
        1. List each symptom and identify possible causes.
        2. Map symptoms to a medical ontology (e.g., mock SNOMED CT terms for normalization).
        3. Identify temporal patterns from the patient's history.
        Return a structured summary in the following format:
        - Symptom Analysis: [List of symptoms with possible causes]
        - Normalized Terms: [Mock SNOMED CT terms]
        - Temporal Patterns: [Patterns observed]
        - Summary: [Brief conclusion]

        Below are few-shot examples to guide your analysis:

        ### Example 1
        **Input:**
        - Patient: {{ "name": "Alice", "age": 40, "gender": "female", "symptoms": ["fever", "cough", "fatigue"], "medications": ["ibuprofen"] }}
        - History: [{{ "date": "2023-01-10", "condition": "Flu", "treatment": "Rest" }}]

        **Output:**
        - Symptom Analysis:
          - Fever: Possible causes include infection (viral or bacterial), inflammation.
          - Cough: Possible causes include respiratory infection, allergies, asthma.
          - Fatigue: Possible causes include infection, sleep deprivation, chronic illness.
        - Normalized Terms:
          - Fever: "Fever (SNOMED: 386661006)"
          - Cough: "Cough (SNOMED: 49727002)"
          - Fatigue: "Fatigue (SNOMED: 84229001)"
        - Temporal Patterns:
          - History shows a past flu episode 2 years ago, suggesting possible recurrence or seasonal pattern.
        - Summary: The symptoms suggest a likely respiratory infection (e.g., flu or pneumonia), consistent with past history.

        ### Example 2
        **Input:**
        - Patient: {{ "name": "Bob", "age": 25, "gender": "male", "symptoms": ["headache", "nausea"], "medications": ["paracetamol"] }}
        - History: [{{ "date": "2024-02-15", "condition": "Migraine", "treatment": "Sumatriptan" }}]

        **Output:**
        - Symptom Analysis:
          - Headache: Possible causes include migraine, tension headache, dehydration.
          - Nausea: Possible causes include migraine, gastrointestinal issue, motion sickness.
        - Normalized Terms:
          - Headache: "Headache (SNOMED: 25064002)"
          - Nausea: "Nausea (SNOMED: 422587007)"
        - Temporal Patterns:
          - History indicates a migraine 13 months ago, suggesting a chronic or recurring condition.
        - Summary: The symptoms align with a possible migraine recurrence, supported by prior history.

        ### Example 3
        **Input:**
        - Patient: {{ "name": "Clara", "age": 60, "gender": "female", "symptoms": ["chest pain", "shortness of breath"], "medications": ["aspirin"] }}
        - History: [{{ "date": "2022-06-20", "condition": "Hypertension", "treatment": "Lisinopril" }}]

        **Output:**
        - Symptom Analysis:
          - Chest pain: Possible causes include cardiac (e.g., angina, myocardial infarction), musculoskeletal, gastrointestinal.
          - Shortness of breath: Possible causes include cardiac (e.g., heart failure), pulmonary (e.g., COPD), anxiety.
        - Normalized Terms:
          - Chest pain: "Chest pain (SNOMED: 29857009)"
          - Shortness of breath: "Dyspnea (SNOMED: 267036007)"
        - Temporal Patterns:
          - History of hypertension 3 years ago may indicate a cardiovascular risk factor.
        - Summary: Symptoms suggest a potential cardiac issue (e.g., angina or heart attack), possibly linked to hypertension history.

        ---

        Now, analyze the following patient data:

        **Input:**
        - Patient: {patient_data}
        - History: {history}

        Provide your analysis in the specified structured format.
        """
        openai = OpenAIWrapper()
        response = openai.get_completion(prompt)
        return response