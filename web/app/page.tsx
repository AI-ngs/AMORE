"use client"

import { useState } from "react"
import { DashboardHeader } from "@/components/dashboard/dashboard-header"
import { DashboardFilters } from "@/components/dashboard/dashboard-filters"
import { ProductGrid } from "@/components/dashboard/product-grid"
import { ExportModal } from "@/components/modals/export-modal"
import { LoadingTransition } from "@/components/loading/loading-transition"
import { ProductDetailView } from "@/components/product-detail/product-detail-view"
import type { Platform, Product } from "@/types/product"

export default function Page() {
  const [selectedPlatform, setSelectedPlatform] = useState<Platform>("@cosme")
  const [selectedCategory, setSelectedCategory] = useState<string>("all")
  const [isExportModalOpen, setIsExportModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)

  const handleProductClick = (product: Product) => {
    setIsLoading(true)
    setTimeout(() => {
      setSelectedProduct(product)
      setIsLoading(false)
    }, 2000)
  }

  const handleBackToDashboard = () => {
    setSelectedProduct(null)
  }

  if (isLoading) {
    return <LoadingTransition />
  }

  if (selectedProduct) {
    return <ProductDetailView product={selectedProduct} onBack={handleBackToDashboard} />
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <DashboardHeader onExportClick={() => setIsExportModalOpen(true)} />

        <DashboardFilters
          selectedPlatform={selectedPlatform}
          selectedCategory={selectedCategory}
          onPlatformChange={setSelectedPlatform}
          onCategoryChange={setSelectedCategory}
        />

        <ProductGrid platform={selectedPlatform} category={selectedCategory} onProductClick={handleProductClick} />

        <ExportModal isOpen={isExportModalOpen} onClose={() => setIsExportModalOpen(false)} />
      </div>
    </div>
  )
}
