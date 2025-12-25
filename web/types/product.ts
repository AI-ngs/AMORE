export type Platform = "@cosme" | "Amazon"

export interface Product {
  id: string
  name: string
  platform: Platform
  category: string
  currentRank: number
  rankChange: number
  imageUrl: string
  totalReviews: number
}
