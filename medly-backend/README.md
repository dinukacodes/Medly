# Healthcare Diagnostic Backend

A FastAPI-based backend for healthcare diagnostics using Crew AI.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt 

to run the backend you have to run the following command
   python main.py

# Guide to Test the Healthcare Diagnostic Backend System with API Calls

This guide provides a detailed, step-by-step process to test the Healthcare Diagnostic Backend system using API calls. We will use `curl` commands to interact with the system's API endpoints, assuming the backend is running locally on `http://localhost:8000`. This guide covers uploading evidence, starting a diagnosis session, streaming diagnosis reasoning, submitting feedback, and retrieving patient history. Sample `curl` commands and expected responses are included for each step.

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
- **Explanation**: Each `data:` line represents a reasoning step (e.g., processing evidence, analyzing symptoms). The stream continues until the diagnosis is complete. Timestamps and details depend on the backend’s implementation.
- **Tip**: To stop the stream, press `Ctrl+C` in the terminal.

---

## Step 4: Submit Feedback

After reviewing the diagnosis, submit feedback to log your interaction. This step is optional but helps test the feedback endpoint.

### Curl Command
```bash
curl -X POST "http://localhost:8000/api/submit-feedback" -H "Content-Type: application/json" -d '{
  "session_id": "unique_session_id",
  "action": "accept",
  "feedback": "The diagnosis seems accurate based on the provided evidence."
}'
```
- Replace `unique_session_id` with the actual `session_id`.
- `action`: Options like `accept`, `reject`, or custom values defined by the backend.
- `feedback`: A text comment on the diagnosis.

### Expected Response
```json
{
  "status": "submitted"
}
```
- **Explanation**: Confirms the feedback was successfully recorded.

---

## Step 5: Retrieve Patient History (Optional)

Test the patient history endpoint by retrieving past medical records for the patient, if available.

### Curl Command
```bash
curl "http://localhost:8000/api/patient-history/John%20Doe"
```
- `John%20Doe`: URL-encoded patient name (space replaced with `%20`).

### Expected Response
```json
{
  "name": "John Doe",
  "history": [
    {
      "date": "2022-01-15",
      "condition": "Flu",
      "treatment": "Oseltamivir"
    },
    {
      "date": "2023-03-10",
      "condition": "Hypertension",
      "treatment": "Lisinopril"
    }
  ]
}
```
- **Explanation**: Returns the patient’s medical history. If no history exists, you may get an empty `history` array (`[]`). To populate history, you might need to manually insert records into the database using SQL (not covered here).

---

## Troubleshooting

If you encounter issues, try these solutions:

- **No Response from Streaming Endpoint**:
  - Verify the `session_id` is correct.
  - Check server logs (in the terminal where `uvicorn` is running) for errors like model failures or processing delays.
- **File Upload Fails**:
  - Ensure the file path in `-F "files=@sample_evidence.pdf"` is correct. Use an absolute path if needed (e.g., `/path/to/sample_evidence.pdf`).
  - Confirm the file exists and is readable.
- **Database Errors**:
  - Ensure the database is initialized with required tables (e.g., for patient history). Check your backend’s setup instructions.
- **Server Not Running**:
  - Confirm the server is active on `http://localhost:8000`. Test with `curl http://localhost:8000` (response depends on root endpoint setup).

---

## Conclusion

This guide walks you through testing the Healthcare Diagnostic Backend system using API calls with `curl`. By executing these steps—uploading evidence, starting a diagnosis, streaming reasoning, submitting feedback, and retrieving history—you can verify the system’s core functionality. Customize patient data and evidence files to test various scenarios. If all steps return expected responses, the system is working correctly!