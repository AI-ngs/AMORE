import { Card } from "@/components/ui/card"
import { Sparkles } from "lucide-react"
import { ReviewAnalysis } from "./review-analysis"
import { SnsViral } from "./sns-viral"
import type { Product } from "@/types/product"

interface DeepInsightProps {
  product: Product
}

export function DeepInsight({ product }: DeepInsightProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="mb-4 text-xl font-semibold text-foreground">Deep Insight</h2>

        <Card className="border-l-4 border-l-sky-500 bg-gradient-to-r from-sky-50 to-white p-6">
          <div className="mb-4 flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-sky-600" />
            <h3 className="text-lg font-bold text-foreground">AI Insight Summary</h3>
          </div>
          <p className="text-sm leading-relaxed text-muted-foreground">
            This product shows strong upward momentum with consistent positive reviews. The hydration benefits are
            particularly well-received by customers aged 25-40.
          </p>
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold text-foreground">AI-Based Detailed Analysis</h3>
        <div className="space-y-3 text-sm leading-relaxed text-muted-foreground">
          <p>
            Based on comprehensive data analysis, this product demonstrates exceptional performance in the skincare
            category. The ranking improvement of +5 positions indicates growing consumer interest and satisfaction.
          </p>
          <p>
            Key drivers include superior hydration technology, elegant packaging design, and competitive pricing
            strategy. Social media engagement shows 240% increase in mentions over the past month.
          </p>
        </div>
      </Card>

      <ReviewAnalysis />
      <SnsViral />
    </div>
  )
}
