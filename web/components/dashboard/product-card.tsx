"use client"

import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import { Card } from "@/components/ui/card"
import type { Product } from "@/types/product"

interface ProductCardProps {
  product: Product
  onClick: () => void
}

export function ProductCard({ product, onClick }: ProductCardProps) {
  const getTrendIcon = () => {
    if (product.rankChange > 0) {
      return <TrendingUp className="h-4 w-4 text-emerald-600" />
    } else if (product.rankChange < 0) {
      return <TrendingDown className="h-4 w-4 text-red-600" />
    }
    return <Minus className="h-4 w-4 text-muted-foreground" />
  }

  const getTrendColor = () => {
    if (product.rankChange > 0) return "text-emerald-600"
    if (product.rankChange < 0) return "text-red-600"
    return "text-muted-foreground"
  }

  return (
    <Card onClick={onClick} className="group cursor-pointer overflow-hidden transition-all hover:shadow-lg">
      <div className="aspect-square overflow-hidden bg-muted">
        <img
          src={product.imageUrl || "/placeholder.svg"}
          alt={product.name}
          className="h-full w-full object-cover transition-transform group-hover:scale-105"
        />
      </div>
      <div className="p-4">
        <h3 className="mb-2 line-clamp-2 text-sm font-medium text-foreground">{product.name}</h3>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs text-muted-foreground">Current Rank</p>
            <p className="text-2xl font-bold text-sky-600">#{product.currentRank}</p>
          </div>
          <div className="flex items-center gap-1">
            {getTrendIcon()}
            <span className={`text-sm font-semibold ${getTrendColor()}`}>{Math.abs(product.rankChange)}</span>
          </div>
        </div>
      </div>
    </Card>
  )
}
