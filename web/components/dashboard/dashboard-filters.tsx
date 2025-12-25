"use client"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CATEGORIES_BY_PLATFORM } from "@/lib/constants/categories"
import type { Platform } from "@/types/product"

interface DashboardFiltersProps {
  selectedPlatform: Platform
  selectedCategory: string
  onPlatformChange: (platform: Platform) => void
  onCategoryChange: (category: string) => void
}

export function DashboardFilters({
  selectedPlatform,
  selectedCategory,
  onPlatformChange,
  onCategoryChange,
}: DashboardFiltersProps) {
  const categories = CATEGORIES_BY_PLATFORM[selectedPlatform]

  return (
    <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center">
      <div className="flex gap-2 rounded-lg border border-border bg-muted/30 p-1">
        <button
          onClick={() => onPlatformChange("@cosme")}
          className={`rounded-md px-6 py-2 text-sm font-medium transition-colors ${
            selectedPlatform === "@cosme"
              ? "bg-sky-500 text-white shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          }`}
        >
          @cosme
        </button>
        <button
          onClick={() => onPlatformChange("Amazon")}
          className={`rounded-md px-6 py-2 text-sm font-medium transition-colors ${
            selectedPlatform === "Amazon"
              ? "bg-sky-500 text-white shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          }`}
        >
          Amazon
        </button>
      </div>

      <Select value={selectedCategory} onValueChange={onCategoryChange}>
        <SelectTrigger className="w-full sm:w-64">
          <SelectValue placeholder="Select category" />
        </SelectTrigger>
        <SelectContent>
          {categories.map((category) => (
            <SelectItem key={category} value={category}>
              {category}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
