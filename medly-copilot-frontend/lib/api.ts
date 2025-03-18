import type { PatientData, SessionResponse, FeedbackResponse } from "./types"

const API_BASE_URL = "/api"

// Start a new diagnosis session
export async function startDiagnosis(
  patientData: PatientData,
  model: "gpt-4o" | "deepseek",
  uploads: File[] = [],
): Promise<SessionResponse> {
  const formData = new FormData()

  // Add patient data
  formData.append(
    "patient",
    JSON.stringify({
      name: patientData.name || "Anonymous",
      age: patientData.age,
      gender: patientData.gender,
      symptoms: patientData.symptoms,
      pastMedicalHistory: patientData.pastMedicalHistory,
      currentMedications: patientData.currentMedications,
    }),
  )

  // Add model selection
  formData.append("model", model)

  // Add any uploaded files
  uploads.forEach((file, index) => {
    formData.append(`file_${index}`, file)
  })

  const response = await fetch(`${API_BASE_URL}/start-diagnosis`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return await response.json()
}

// Get patient history
export async function getPatientHistory(name: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/patient-history/${encodeURIComponent(name)}`)

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return await response.json()
}

// Submit physician feedback
export async function submitFeedback(
  sessionId: string,
  status: "accept" | "reject",
  feedback: string,
): Promise<FeedbackResponse> {
  const response = await fetch(`${API_BASE_URL}/submit-feedback`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: sessionId,
      status,
      feedback,
    }),
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return await response.json()
}

// Upload evidence files
export async function uploadEvidence(sessionId: string, files: File[]): Promise<any> {
  const formData = new FormData()
  formData.append("session_id", sessionId)

  files.forEach((file, index) => {
    formData.append(`file_${index}`, file)
  })

  const response = await fetch(`${API_BASE_URL}/upload-evidence`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return await response.json()
}

// Create an SSE connection for streaming diagnosis updates
export function streamDiagnosis(
  sessionId: string,
  onMessage: (data: any) => void,
  onError: (error: any) => void,
): () => void {
  const eventSource = new EventSource(`${API_BASE_URL}/stream-diagnosis/${sessionId}`)

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (error) {
      onError(error)
    }
  }

  eventSource.onerror = (error) => {
    onError(error)
    eventSource.close()
  }

  // Return a function to close the connection
  return () => {
    eventSource.close()
  }
}

