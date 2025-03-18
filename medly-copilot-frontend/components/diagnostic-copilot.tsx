"use client"

import { useState, useEffect, useRef } from "react"
import { Header } from "@/components/header"
import { InputPanel } from "@/components/input-panel"
import { OutputPanel } from "@/components/output-panel"
import { Footer } from "@/components/footer"
import { startDiagnosis, streamDiagnosis, submitFeedback } from "@/lib/api"
import type { PatientData, AnalysisResult, DiagnosticStep } from "@/lib/types"

export function DiagnosticCopilot() {
  const [selectedModel, setSelectedModel] = useState<"gpt-4o" | "deepseek">("gpt-4o")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [elapsedTime, setElapsedTime] = useState(0)
  const [diagnosisStatus, setDiagnosisStatus] = useState<"pending" | "required" | "approved">("pending")
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [diagnosticSteps, setDiagnosticSteps] = useState<DiagnosticStep[]>([])
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])

  const eventSourceRef = useRef<(() => void) | null>(null)

  // Timer for the 15-minute consultation
  useEffect(() => {
    let interval: NodeJS.Timeout

    if (isAnalyzing || diagnosisStatus !== "pending") {
      interval = setInterval(() => {
        setElapsedTime((prev) => prev + 1)
      }, 1000)
    }

    return () => clearInterval(interval)
  }, [isAnalyzing, diagnosisStatus])

  // Simulate progress bar during analysis based on diagnostic steps
  useEffect(() => {
    if (isAnalyzing) {
      // Calculate progress based on the number of steps received
      // Assuming a total of 5 steps in the pipeline
      const stepProgress = diagnosticSteps.length > 0 ? (diagnosticSteps.length / 5) * 100 : 0
      setProgress(Math.min(stepProgress, 95)) // Cap at 95% until complete
    } else if (analysisResult) {
      setProgress(100) // Set to 100% when analysis is complete
    }
  }, [isAnalyzing, diagnosticSteps, analysisResult])

  // Reset progress when not analyzing
  useEffect(() => {
    if (!isAnalyzing) {
      setProgress(0)
    }
  }, [isAnalyzing])

  // Clean up event source on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current()
      }
    }
  }, [])

  const handleAnalyzePatientData = async (patientData: PatientData) => {
    setIsAnalyzing(true)
    setDiagnosisStatus("pending")
    setDiagnosticSteps([])
    setAnalysisResult(null)

    try {
      // Start a new diagnosis session
      const response = await startDiagnosis(patientData, selectedModel, uploadedFiles)
      setSessionId(response.session_id)

      // Set up SSE connection for streaming updates
      if (eventSourceRef.current) {
        eventSourceRef.current() // Close existing connection
      }

      eventSourceRef.current = streamDiagnosis(
        response.session_id,
        (data) => {
          if (data.step) {
            // This is a diagnostic step update
            setDiagnosticSteps((prev) => [...prev, data])
          } else if (data.differentials) {
            // This is the final result
            setAnalysisResult(data)
            setDiagnosisStatus("required")
            setIsAnalyzing(false)

            // Close the SSE connection
            if (eventSourceRef.current) {
              eventSourceRef.current()
              eventSourceRef.current = null
            }
          }
        },
        (error) => {
          console.error("SSE error:", error)
          setIsAnalyzing(false)
        },
      )
    } catch (error) {
      console.error("Error analyzing patient data:", error)
      setIsAnalyzing(false)
    }
  }

  const handleAcceptDiagnosis = async () => {
    if (sessionId) {
      try {
        await submitFeedback(sessionId, "accept", "")
        setDiagnosisStatus("approved")
      } catch (error) {
        console.error("Error accepting diagnosis:", error)
      }
    }
  }

  const handleRejectDiagnosis = async () => {
    if (sessionId) {
      try {
        await submitFeedback(sessionId, "reject", "")
        // In a real app, this would open a modification interface
        // For demo purposes, we'll just reset to required
        setDiagnosisStatus("required")
      } catch (error) {
        console.error("Error rejecting diagnosis:", error)
      }
    }
  }

  const handleSubmitFeedback = async (feedback: string) => {
    if (sessionId) {
      try {
        await submitFeedback(sessionId, diagnosisStatus === "approved" ? "accept" : "reject", feedback)
      } catch (error) {
        console.error("Error submitting feedback:", error)
      }
    }
  }

  const handleFileUpload = (files: File[]) => {
    setUploadedFiles(files)
  }

  return (
    <div className="flex flex-col h-screen">
      <Header selectedModel={selectedModel} onModelChange={setSelectedModel} />

      <div className="flex flex-col md:flex-row flex-1 p-4 gap-4 overflow-hidden">
        <InputPanel
          onAnalyze={handleAnalyzePatientData}
          isAnalyzing={isAnalyzing}
          diagnosisStatus={diagnosisStatus}
          onAcceptDiagnosis={handleAcceptDiagnosis}
          onRejectDiagnosis={handleRejectDiagnosis}
          onSubmitFeedback={handleSubmitFeedback}
          onFileUpload={handleFileUpload}
        />

        <OutputPanel
          isAnalyzing={isAnalyzing}
          progress={progress}
          analysisResult={analysisResult}
          diagnosisStatus={diagnosisStatus}
          diagnosticSteps={diagnosticSteps}
        />
      </div>

      <Footer diagnosisStatus={diagnosisStatus} elapsedTime={elapsedTime} />
    </div>
  )
}

