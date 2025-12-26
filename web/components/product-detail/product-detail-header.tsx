import { Badge } from "@/components/ui/badge"
import type { Product } from "@/types/product"

interface ProductDetailHeaderProps {
  product: Product
}

export function ProductDetailHeader({ product }: ProductDetailHeaderProps) {
  return (
    <div className="flex items-center gap-4">
      <div className="h-16 w-16 overflow-hidden rounded-lg bg-muted">
        <img src={product.imageUrl || "/placeholder.svg"} alt={product.name} className="h-full w-full object-cover" />
      </div>
      <div className="flex-1">
        <h1 className="text-2xl font-bold text-foreground">{product.name}</h1>
        <Badge variant="secondary" className="mt-1">
          {product.platform}
        </Badge>
      </div>
    </div>
  )
}
