"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, CheckCircle, AlertCircle, Upload, X } from "lucide-react"
import type { PatientData } from "@/lib/types"
import { cn } from "@/lib/utils"

interface InputPanelProps {
  onAnalyze: (patientData: PatientData) => void
  isAnalyzing: boolean
  diagnosisStatus: "pending" | "required" | "approved"
  onAcceptDiagnosis: () => void
  onRejectDiagnosis: () => void
  onSubmitFeedback: (feedback: string) => void
  onFileUpload: (files: File[]) => void
}

export function InputPanel({
  onAnalyze,
  isAnalyzing,
  diagnosisStatus,
  onAcceptDiagnosis,
  onRejectDiagnosis,
  onSubmitFeedback,
  onFileUpload,
}: InputPanelProps) {
  const [patientData, setPatientData] = useState<PatientData>({
    name: "",
    age: "",
    gender: "",
    symptoms: "",
    pastMedicalHistory: "",
    currentMedications: "",
  })
  const [feedback, setFeedback] = useState("")
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setPatientData((prev) => ({ ...prev, [name]: value }))
  }

  const handleAnalyze = () => {
    onAnalyze(patientData)
  }

  const handleSubmitFeedback = () => {
    onSubmitFeedback(feedback)
    setFeedback("")
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const filesArray = Array.from(e.target.files)
      setUploadedFiles((prev) => [...prev, ...filesArray])
      onFileUpload([...uploadedFiles, ...filesArray])
    }
  }

  const handleRemoveFile = (index: number) => {
    const newFiles = [...uploadedFiles]
    newFiles.splice(index, 1)
    setUploadedFiles(newFiles)
    onFileUpload(newFiles)
  }

  const triggerFileUpload = () => {
    fileInputRef.current?.click()
  }

  return (
    <Card className="w-full md:w-1/2 flex flex-col">
      <CardHeader>
        <CardTitle className="text-blue-700">Patient Information</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Patient Name</Label>
          <Input
            id="name"
            name="name"
            placeholder="e.g., John Doe"
            value={patientData.name}
            onChange={handleInputChange}
            disabled={isAnalyzing}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="age">Age</Label>
            <Input
              id="age"
              name="age"
              type="number"
              placeholder="e.g., 45"
              value={patientData.age}
              onChange={handleInputChange}
              disabled={isAnalyzing}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="gender">Gender</Label>
            <Input
              id="gender"
              name="gender"
              placeholder="e.g., Male"
              value={patientData.gender}
              onChange={handleInputChange}
              disabled={isAnalyzing}
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="symptoms">Symptoms</Label>
          <Textarea
            id="symptoms"
            name="symptoms"
            placeholder="Describe patient symptoms..."
            rows={3}
            value={patientData.symptoms}
            onChange={handleInputChange}
            disabled={isAnalyzing}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="pastMedicalHistory">Past Medical History</Label>
          <Textarea
            id="pastMedicalHistory"
            name="pastMedicalHistory"
            placeholder="Relevant medical history..."
            rows={3}
            value={patientData.pastMedicalHistory}
            onChange={handleInputChange}
            disabled={isAnalyzing}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="currentMedications">Current Medications</Label>
          <Textarea
            id="currentMedications"
            name="currentMedications"
            placeholder="List current medications..."
            rows={3}
            value={patientData.currentMedications}
            onChange={handleInputChange}
            disabled={isAnalyzing}
          />
        </div>

        {/* File Upload Section */}
        <div className="space-y-2">
          <Label>Evidence Files (X-rays, Lab Results, etc.)</Label>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            multiple
            disabled={isAnalyzing}
          />
          <Button type="button" variant="outline" className="w-full" onClick={triggerFileUpload} disabled={isAnalyzing}>
            <Upload className="mr-2 h-4 w-4" />
            Upload Files
          </Button>

          {uploadedFiles.length > 0 && (
            <div className="mt-2 space-y-2">
              {uploadedFiles.map((file, index) => (
                <div key={index} className="flex items-center justify-between bg-slate-50 p-2 rounded-md">
                  <span className="text-sm truncate">{file.name}</span>
                  <Button variant="ghost" size="sm" onClick={() => handleRemoveFile(index)} disabled={isAnalyzing}>
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </div>

        <Button className="w-full" onClick={handleAnalyze} disabled={isAnalyzing || diagnosisStatus !== "pending"}>
          {isAnalyzing ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Analyzing Patient Data...
            </>
          ) : (
            "Analyze Patient Data"
          )}
        </Button>

        {diagnosisStatus !== "pending" && (
          <div className="mt-6 space-y-4 border-t pt-4">
            <div>
              <h3 className="text-sm font-medium text-slate-700 mb-2">Physician Feedback</h3>
              <Textarea
                placeholder="Enter your feedback on the diagnosis..."
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                rows={3}
              />
            </div>

            <div className="flex flex-col sm:flex-row gap-2">
              <Button
                variant="outline"
                className={cn("flex-1", diagnosisStatus === "approved" && "bg-green-50 border-green-200")}
                onClick={onAcceptDiagnosis}
                disabled={diagnosisStatus === "approved"}
              >
                <CheckCircle
                  className={cn("mr-2 h-4 w-4", diagnosisStatus === "approved" ? "text-green-500" : "text-slate-400")}
                />
                Accept Diagnosis
              </Button>
              <Button variant="outline" className="flex-1" onClick={onRejectDiagnosis}>
                <AlertCircle className="mr-2 h-4 w-4 text-amber-500" />
                Reject & Modify
              </Button>
            </div>

            <Button className="w-full" onClick={handleSubmitFeedback} disabled={!feedback.trim()}>
              Submit Feedback
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

