export interface PatientData {
  name?: string
  age: string
  gender: string
  symptoms: string
  pastMedicalHistory: string
  currentMedications: string
}

export interface SessionResponse {
  session_id: string
}

export interface FeedbackResponse {
  status: string
}

export interface DiagnosticStep {
  step: string
  text: string
  data?: any
}

export interface Diagnosis {
  diagnosis: string
  probability: number
  justification: string
}

export interface Evidence {
  source: string
  relevance: string
  text: string
}

export interface Treatment {
  treatment: string
  dosage: string
  warnings: string
}

export interface AnalysisResult {
  differentials: Diagnosis[]
  evidence: string
  treatment: string
  treatmentDetails?: Treatment
  evidenceDetails?: Evidence[]
  supportingLiterature?: string[]
}

