import { Card } from "@/components/ui/card"
import { ThumbsUp, ThumbsDown } from "lucide-react"

export function ReviewAnalysis() {
  return (
    <Card className="p-6">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Customer Review Deep Analysis</h3>

      <div className="mb-4">
        <p className="text-sm leading-relaxed text-muted-foreground">
          Comprehensive analysis of 2,847 customer reviews reveals consistent satisfaction with product efficacy and
          user experience.
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <div className="mb-2 flex items-center gap-2">
            <ThumbsUp className="h-4 w-4 text-emerald-600" />
            <h4 className="font-semibold text-foreground">Pros</h4>
          </div>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• Excellent hydration lasting 24+ hours</li>
            <li>• Lightweight, non-greasy texture absorbs quickly</li>
            <li>• Visible improvement in skin brightness within 2 weeks</li>
          </ul>
        </div>

        <div>
          <div className="mb-2 flex items-center gap-2">
            <ThumbsDown className="h-4 w-4 text-red-600" />
            <h4 className="font-semibold text-foreground">Cons (Improvement Points)</h4>
          </div>
          <ul className="space-y-1 text-sm text-muted-foreground">
            <li>• Packaging could be more travel-friendly</li>
            <li>• Price point considered high for smaller sizes</li>
            <li>• Scent may be too strong for sensitive individuals</li>
          </ul>
        </div>
      </div>
    </Card>
  )
}
