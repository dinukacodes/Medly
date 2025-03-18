# Medly Backend

A FastAPI-based backend for Medly using Crew AI.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt 
   ```
   
To run the backend, use the following command:
   ```bash
   python main.py
   ```

# Guide to Test the Medly Backend System with API Calls

This guide provides a detailed, step-by-step process to test the Medly Backend system using API calls. We will use `curl` commands to interact with the system's API endpoints, assuming the backend is running locally on `http://localhost:8000`. This guide covers uploading evidence, starting a diagnosis session, streaming diagnosis reasoning, submitting feedback, and retrieving patient history. Sample `curl` commands and expected responses are included for each step.

---

## Prerequisites

Before testing the system, ensure the following are in place:

1. **Start the Backend Server**:
   - Open a terminal and navigate to the project directory containing the FastAPI application (e.g., where `main.py` is located).
   - Run the following command to start the server:
     ```bash
     uvicorn main:app --reload
     ```
   - This command starts the FastAPI server on `http://localhost:8000` with auto-reload enabled for development. Confirm the server is running by checking the terminal output for a message like `Application startup complete`.

2. **Install `curl`**:
   - Ensure `curl` is installed on your system. On most Linux/macOS systems, it’s pre-installed. For Windows, you can download it or use a terminal like Git Bash or WSL.
   - Verify installation by running:
     ```bash
     curl --version
     ```

3. **Prepare Sample Data**:
   - **Evidence File**: Create a sample PDF file named `sample_evidence.pdf`. You can create it with any text editor or tool (e.g., save "Test medical report" as a PDF). Place it in an accessible directory.
   - **Research Papers**: Ensure the `research_papers` directory (if used by the backend’s RAG system) contains at least one PDF file. This is optional and depends on your backend configuration.

---

## Step 1: Upload Evidence

The first step is to upload a sample evidence file (e.g., a medical report) to the backend. This simulates a user submitting lab results or imaging studies.

### Curl Command
```bash
curl -X POST "http://localhost:8000/api/upload-evidence" -F "files=@sample_evidence.pdf"
```
- `-X POST`: Specifies a POST request.
- `-F "files=@sample_evidence.pdf"`: Uploads the file using form-data syntax. Ensure the file path is correct relative to your current directory.

### Expected Response
```json
{
  "file_ids": ["unique_file_id"],
  "status": "uploaded"
}
```
- **Explanation**: The response includes a `file_ids` array with a unique identifier for the uploaded file (e.g., a UUID like `123e4567-e89b-12d3-a456-426614174000`) and a status confirming the upload.
- **Action**: Note down the `file_id` (e.g., `unique_file_id`). You’ll need it for the next step.

---

## Step 2: Start a Diagnosis Session

Next, initiate a diagnosis session by sending patient data and the evidence file ID from Step 1. This step triggers the backend to process the input and begin the diagnosis.

### Curl Command
```bash
curl -X POST "http://localhost:8000/api/start-diagnosis" -H "Content-Type: application/json" -d '{
  "model": "gpt-4o",
  "patient": {
    "name": "John Doe",
    "age": 45,
    "gender": "male",
    "symptoms": ["fever", "cough", "fatigue"],
    "medications": ["ibuprofen"]
  },
  "evidence": ["unique_file_id"]
}'
```
- `-H "Content-Type: application/json"`: Sets the request header to indicate JSON data.
- `-d '{...}'`: The JSON payload includes:
  - `model`: The AI model to use (e.g., `gpt-4o`).
  - `patient`: Patient details like name, age, gender, symptoms, and medications.
  - `evidence`: An array containing the `file_id` from Step 1 (replace `unique_file_id` with the actual ID).

### Expected Response
```json
{
  "session_id": "unique_session_id",
  "status": "started"
}
```
- **Explanation**: The response provides a `session_id` (e.g., `abc123-def456`) and confirms the session has started.
- **Action**: Note down the `session_id`. It’s required for streaming the diagnosis in the next step.

---

## Step 3: Stream Diagnosis Reasoning Steps

Use the session ID to stream the diagnosis reasoning process in real-time. This endpoint uses Server-Sent Events (SSE) to push updates as the backend analyzes the data.

### Curl Command
```bash
curl "http://localhost:8000/api/stream-diagnosis/unique_session_id"
```
- Replace `unique_session_id` with the actual `session_id` from Step 2.

### Expected Output
The response will be a continuous stream of SSE messages, each prefixed with `data:`:
```
data: 2024-10-18 12:34:56: Evidence processed: [extracted text from PDF]

data: 2024-10-18 12:35:00: Symptom analysis: [analysis details]

data: 2024-10-18 12:35:05: Evidence evaluation: [evaluation details]

...
```

... (Rest of the document remains the same)

