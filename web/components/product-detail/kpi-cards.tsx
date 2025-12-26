import { Card } from "@/components/ui/card"
import { TrendingUp, TrendingDown, MessageSquare } from "lucide-react"
import type { Product } from "@/types/product"

interface KpiCardsProps {
  product: Product
}

export function KpiCards({ product }: KpiCardsProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <Card className="border-l-4 border-l-sky-500 p-4">
        <div className="flex items-center gap-3">
          <div className="rounded-full bg-sky-100 p-2">
            <TrendingUp className="h-5 w-5 text-sky-600" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Current Ranking</p>
            <p className="text-2xl font-bold text-sky-600">#{product.currentRank}</p>
          </div>
        </div>
      </Card>

      <Card className="border-l-4 border-l-emerald-500 p-4">
        <div className="flex items-center gap-3">
          <div className="rounded-full bg-emerald-100 p-2">
            {product.rankChange >= 0 ? (
              <TrendingUp className="h-5 w-5 text-emerald-600" />
            ) : (
              <TrendingDown className="h-5 w-5 text-red-600" />
            )}
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Rank Change</p>
            <p className={`text-2xl font-bold ${product.rankChange >= 0 ? "text-emerald-600" : "text-red-600"}`}>
              {product.rankChange > 0 ? "+" : ""}
              {product.rankChange}
            </p>
          </div>
        </div>
      </Card>

      <Card className="border-l-4 border-l-violet-500 p-4">
        <div className="flex items-center gap-3">
          <div className="rounded-full bg-violet-100 p-2">
            <MessageSquare className="h-5 w-5 text-violet-600" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Total Reviews</p>
            <p className="text-2xl font-bold text-violet-600">{product.totalReviews.toLocaleString()}</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
