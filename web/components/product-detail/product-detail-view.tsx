"use client"

import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ProductDetailHeader } from "./product-detail-header"
import { BasicAnalysis } from "./basic-analysis"
import { DeepInsight } from "./deep-insight"
import type { Product } from "@/types/product"

interface ProductDetailViewProps {
  product: Product
  onBack: () => void
}

export function ProductDetailView({ product, onBack }: ProductDetailViewProps) {
  return (
    <div className="min-h-screen bg-white">
      <div className="mx-auto max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">
        <Button variant="ghost" onClick={onBack} className="mb-6 gap-2 text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-4 w-4" />
          Back to Dashboard
        </Button>

        <ProductDetailHeader product={product} />

        <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
          <BasicAnalysis product={product} />
          <DeepInsight product={product} />
        </div>
      </div>
    </div>
  )
}
