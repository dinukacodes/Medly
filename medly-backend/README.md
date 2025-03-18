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
  "status":
