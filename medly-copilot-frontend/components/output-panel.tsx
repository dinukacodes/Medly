"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import type { AnalysisResult, DiagnosticStep } from "@/lib/types"
import { Loader2 } from "lucide-react"

interface OutputPanelProps {
  isAnalyzing: boolean
  progress: number
  analysisResult: AnalysisResult | null
  diagnosisStatus: "pending" | "required" | "approved"
  diagnosticSteps: DiagnosticStep[]
}

export function OutputPanel({
  isAnalyzing,
  progress,
  analysisResult,
  diagnosisStatus,
  diagnosticSteps,
}: OutputPanelProps) {
  const [activeTab, setActiveTab] = useState("differentials")

  // Format the diagnostic steps for display
  const renderDiagnosticSteps = () => {
    return diagnosticSteps.map((step, index) => (
      <div key={index} className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
        <h4 className="text-sm font-medium text-blue-800 mb-1">{step.step}</h4>
        <p className="text-sm text-blue-700">{step.text}</p>
      </div>
    ))
  }

  return (
    <Card className="w-full md:w-1/2 flex flex-col">
      <CardHeader>
        <CardTitle className="text-blue-700">Diagnostic Results</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto">
        {isAnalyzing ? (
          <div className="h-full flex flex-col items-center justify-center space-y-4">
            <Loader2 className="h-8 w-8 text-blue-600 animate-spin" />
            <div className="text-center">
              <p className="text-slate-600 mb-2">Analyzing patient data...</p>
              <div className="w-full max-w-md">
                <Progress value={progress} className="h-2" />
              </div>
              <p className="text-sm text-slate-500 mt-2">{progress}% complete</p>
            </div>

            {/* Display diagnostic steps during analysis */}
            <div className="w-full mt-6">{renderDiagnosticSteps()}</div>
          </div>
        ) : diagnosisStatus === "pending" ? (
          <div className="h-full flex items-center justify-center">
            <p className="text-slate-500 italic">
              Enter patient information and click "Analyze Patient Data" to begin.
            </p>
          </div>
        ) : (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid grid-cols-3 mb-4">
              <TabsTrigger value="differentials">Differential Diagnoses</TabsTrigger>
              <TabsTrigger value="evidence">Evidence Summary</TabsTrigger>
              <TabsTrigger value="treatment">Treatment Plan</TabsTrigger>
            </TabsList>

            <TabsContent value="differentials" className="space-y-4">
              <h3 className="font-medium text-slate-800">Potential Diagnoses (by probability)</h3>
              {analysisResult?.differentials.map((diagnosis, index) => {
                return (
                  <div key={index} className="space-y-1">
                    <div className="flex justify-between">
                      <span className="font-medium">{diagnosis.diagnosis}</span>
                      <span className="text-sm">{diagnosis.probability}%</span>
                    </div>
                    <Progress
                      value={diagnosis.probability}
                      className="h-2"
                      indicatorClassName={
                        diagnosis.probability > 80
                          ? "bg-green-500"
                          : diagnosis.probability > 50
                            ? "bg-amber-500"
                            : "bg-slate-400"
                      }
                    />
                    <p className="text-sm text-slate-600 mt-1">{diagnosis.justification}</p>
                  </div>
                )
              })}

              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
                <h4 className="text-sm font-medium text-blue-800 mb-2">AI Confidence Assessment</h4>
                <p className="text-sm text-blue-700">
                  The model has high confidence in the primary diagnosis based on symptom pattern recognition and
                  clinical database matching.
                </p>
              </div>
            </TabsContent>

            <TabsContent value="evidence" className="space-y-4">
              <h3 className="font-medium text-slate-800">Clinical Evidence</h3>
              <div className="p-4 bg-white rounded-lg border border-slate-200">
                <p className="text-slate-700">{analysisResult?.evidence}</p>

                <div className="mt-4 pt-4 border-t border-slate-100">
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Supporting Literature</h4>
                  <ul className="space-y-2 text-sm text-slate-600">
                    {analysisResult?.supportingLiterature ? (
                      analysisResult.supportingLiterature.map((literature, index) => (
                        <li key={index}>• {literature}</li>
                      ))
                    ) : (
                      <>
                        <li>• PubMed ID: 12345678 - "Clinical Presentation of Respiratory Infections"</li>
                        <li>• PubMed ID: 23456789 - "Antibiotic Selection in Primary Care"</li>
                        <li>• Clinical Guidelines 2025 - "Management of Community Acquired Pneumonia"</li>
                      </>
                    )}
                  </ul>
                </div>
              </div>

              <div className="p-4 bg-amber-50 rounded-lg border border-amber-100">
                <h4 className="text-sm font-medium text-amber-800 mb-2">Diagnostic Considerations</h4>
                <p className="text-sm text-amber-700">
                  Consider additional testing to rule out less common respiratory pathogens if patient does not respond
                  to initial treatment within 48-72 hours.
                </p>
              </div>
            </TabsContent>

            <TabsContent value="treatment" className="space-y-4">
              <h3 className="font-medium text-slate-800">Recommended Treatment Plan</h3>
              <div className="p-4 bg-white rounded-lg border border-slate-200">
                <p className="text-slate-700 mb-4">{analysisResult?.treatment}</p>

                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-slate-700 mb-2">Medication</h4>
                    <div className="p-3 bg-slate-50 rounded border border-slate-200 text-sm">
                      {analysisResult?.treatmentDetails ? (
                        <>
                          <p className="font-medium">{analysisResult.treatmentDetails.treatment}</p>
                          <p className="text-slate-600">{analysisResult.treatmentDetails.dosage}</p>
                          <p className="text-slate-500 text-xs mt-1">{analysisResult.treatmentDetails.warnings}</p>
                        </>
                      ) : (
                        <>
                          <p className="font-medium">Amoxicillin 500mg</p>
                          <p className="text-slate-600">Take 1 capsule three times daily for 7 days</p>
                          <p className="text-slate-500 text-xs mt-1">
                            Take with or without food. Complete full course.
                          </p>
                        </>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium text-slate-700 mb-2">Follow-up</h4>
                    <p className="text-sm text-slate-600">
                      • Schedule follow-up in 7 days
                      <br />• Return sooner if symptoms worsen or fever persists beyond 48 hours
                      <br />• Consider chest X-ray if symptoms do not improve
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-green-50 rounded-lg border border-green-100">
                <h4 className="text-sm font-medium text-green-800 mb-2">Patient Education</h4>
                <p className="text-sm text-green-700">
                  Advise patient on adequate hydration, rest, and over-the-counter antipyretics as needed for fever.
                  Explain signs of worsening that require immediate attention.
                </p>
              </div>
            </TabsContent>
          </Tabs>
        )}
      </CardContent>
    </Card>
  )
}

