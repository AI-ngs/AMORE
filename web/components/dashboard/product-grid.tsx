"use client"

import { ProductCard } from "./product-card"
import { MOCK_PRODUCTS } from "@/lib/constants/mock-data"
import type { Platform, Product } from "@/types/product"

interface ProductGridProps {
  platform: Platform
  category: string
  onProductClick: (product: Product) => void
}

export function ProductGrid({ platform, category, onProductClick }: ProductGridProps) {
  const filteredProducts = MOCK_PRODUCTS.filter(
    (product) => product.platform === platform && (category === "all" || product.category === category),
  )

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {filteredProducts.map((product) => (
        <ProductCard key={product.id} product={product} onClick={() => onProductClick(product)} />
      ))}
    </div>
  )
}
