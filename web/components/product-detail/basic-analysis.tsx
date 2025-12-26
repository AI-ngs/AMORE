import { Card } from "@/components/ui/card"
import { KpiCards } from "./kpi-cards"
import { TrendChart } from "./trend-chart"
import { KeywordAnalysis } from "./keyword-analysis"
import { SentimentAnalysis } from "./sentiment-analysis"
import type { Product } from "@/types/product"

interface BasicAnalysisProps {
  product: Product
}

export function BasicAnalysis({ product }: BasicAnalysisProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="mb-4 text-xl font-semibold text-foreground">Basic Analysis</h2>
        <KpiCards product={product} />
      </div>

      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold text-foreground">Ranking Trend (Last 3 Weeks)</h3>
        <TrendChart />
      </Card>

      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold text-foreground">Keyword Analysis</h3>
        <KeywordAnalysis />
      </Card>

      <Card className="p-6">
        <h3 className="mb-4 text-lg font-semibold text-foreground">Sentiment Analysis</h3>
        <SentimentAnalysis />
      </Card>
    </div>
  )
}
