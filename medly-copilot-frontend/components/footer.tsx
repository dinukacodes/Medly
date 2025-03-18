import { cn } from "@/lib/utils"
import { AlertCircle, CheckCircle, Clock } from "lucide-react"

interface FooterProps {
  diagnosisStatus: "pending" | "required" | "approved"
  elapsedTime: number
}

export function Footer({ diagnosisStatus, elapsedTime }: FooterProps) {
  // Format elapsed time as mm:ss
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
  }

  return (
    <footer className="bg-white border-t border-slate-200 py-2">
      <div className="container mx-auto px-4 flex flex-col sm:flex-row items-center justify-between">
        <div className="flex items-center gap-2 mb-2 sm:mb-0">
          {diagnosisStatus === "pending" ? (
            <span className="text-slate-500">Awaiting patient data</span>
          ) : diagnosisStatus === "required" ? (
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-amber-500 mr-2" />
              <span className="text-amber-600 font-medium">Physician Review Required</span>
            </div>
          ) : (
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              <span className="text-green-600 font-medium">Diagnosis Approved</span>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-slate-400" />
          <div className="text-sm">
            <span className={cn("font-medium", elapsedTime > 60 * 10 ? "text-red-500" : "text-slate-600")}>
              {formatTime(elapsedTime)}
            </span>
            <span className="text-slate-400"> / 15:00</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

