import { Card } from "@/components/ui/card"
import { Instagram, ExternalLink } from "lucide-react"

const MOCK_SNS_POSTS = [
  {
    id: 1,
    title: "My night routine with Laneige - Game changer!",
    views: 245600,
    date: "2025-12-20",
  },
  {
    id: 2,
    title: "Laneige vs Premium Brands: Worth the Hype?",
    views: 189300,
    date: "2025-12-18",
  },
  {
    id: 3,
    title: "One week results - Before & After",
    views: 156700,
    date: "2025-12-15",
  },
  {
    id: 4,
    title: "Korean beauty secrets revealed",
    views: 134200,
    date: "2025-12-12",
  },
]

export function SnsViral() {
  return (
    <Card className="p-6">
      <h3 className="mb-4 text-lg font-semibold text-foreground">SNS Viral Posts</h3>

      <div className="space-y-3">
        {MOCK_SNS_POSTS.map((post) => (
          <div
            key={post.id}
            className="group flex items-center justify-between rounded-lg border border-border p-3 transition-colors hover:bg-muted/50"
          >
            <div className="flex items-center gap-3">
              <Instagram className="h-5 w-5 text-pink-600" />
              <div>
                <p className="text-sm font-medium text-foreground">{post.title}</p>
                <div className="mt-1 flex items-center gap-3 text-xs text-muted-foreground">
                  <span>{post.views.toLocaleString()} views</span>
                  <span>•</span>
                  <span>{post.date}</span>
                </div>
              </div>
            </div>
            <ExternalLink className="h-4 w-4 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
          </div>
        ))}
      </div>
    </Card>
  )
}
