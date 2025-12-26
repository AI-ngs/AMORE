import type { Platform } from "@/types/product"

export const CATEGORIES_BY_PLATFORM: Record<Platform, string[]> = {
  "@cosme": ["all", "Skincare", "Makeup", "Body Care", "Hair Care", "Fragrance"],
  Amazon: ["all", "Beauty & Personal Care", "Luxury Beauty", "Skincare", "Makeup", "Tools & Accessories"],
}
