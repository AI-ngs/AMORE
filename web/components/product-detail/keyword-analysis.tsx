import { Badge } from "@/components/ui/badge"

const MOCK_KEYWORDS = [
  "Hydrating",
  "Long-lasting",
  "Smooth texture",
  "Great scent",
  "Affordable",
  "Effective",
  "Gentle",
  "Moisturizing",
]

export function KeywordAnalysis() {
  return (
    <div className="flex flex-wrap gap-2">
      {MOCK_KEYWORDS.map((keyword, index) => (
        <Badge key={index} variant="secondary" className="bg-sky-50 text-sky-700 hover:bg-sky-100">
          {keyword}
        </Badge>
      ))}
    </div>
  )
}
