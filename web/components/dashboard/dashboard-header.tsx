"use client"

import { FileDown } from "lucide-react"
import { Button } from "@/components/ui/button"

interface DashboardHeaderProps {
  onExportClick: () => void
}

export function DashboardHeader({ onExportClick }: DashboardHeaderProps) {
  return (
    <header className="mb-8 flex items-center justify-between">
      <h1 className="text-3xl font-bold text-foreground">Laneige Agent</h1>
      <Button onClick={onExportClick} className="gap-2">
        <FileDown className="h-4 w-4" />
        Excel Export
      </Button>
    </header>
  )
}
