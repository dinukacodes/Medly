"use client"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Stethoscope } from "lucide-react"

interface HeaderProps {
  selectedModel: "gpt-4o" | "deepseek"
  onModelChange: (model: "gpt-4o" | "deepseek") => void
}

export function Header({ selectedModel, onModelChange }: HeaderProps) {
  return (
    <header className="bg-white border-b border-slate-200 shadow-sm">
      <div className="container mx-auto px-4 py-3 flex flex-col sm:flex-row items-center justify-between">
        <div className="flex items-center gap-2 mb-2 sm:mb-0">
          <Stethoscope className="h-6 w-6 text-blue-600" />
          <h1 className="text-xl font-semibold text-slate-800">Medly Diagnostic Co-Pilot</h1>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-slate-500">AI Model:</span>
            <Select value={selectedModel} onValueChange={(value) => onModelChange(value as "gpt-4o" | "deepseek")}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select Model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gpt-4o">Gemini 2.0 Flash</SelectItem>
                <SelectItem value="deepseek">Deepseek-R1 (Local)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="text-sm text-slate-500">
            <span>March 11, 2025</span>
          </div>
        </div>
      </div>
    </header>
  )
}

