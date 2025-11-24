import { Badge } from "@/components/ui/badge"
import { Building2, Calendar } from "lucide-react"
import type { Development } from "@/types"

interface DevelopmentListProps {
  developments?: Development[]
}

export function DevelopmentList({ developments }: DevelopmentListProps) {
  // No fallback data - show empty state if no data
  if (!developments || developments.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <Building2 className="h-12 w-12 mx-auto mb-2 opacity-50" />
        <p className="text-sm">No development data available</p>
        <p className="text-xs mt-1">Development applications will appear when loaded from API</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {developments.map((dev) => (
        <div
          key={dev.id}
          className="flex items-start justify-between p-4 rounded-lg border border-border bg-card hover:bg-accent/50 transition-colors"
        >
          <div className="flex items-start gap-3 flex-1">
            <div className="p-2 rounded-lg bg-primary/10">
              <Building2 className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1">
              <h4 className="font-semibold text-foreground">{dev.address}</h4>
              <p className="text-sm text-muted-foreground mt-1">{dev.name}</p>
              <div className="flex items-center gap-2 mt-2">
                <Badge variant="secondary" className="text-xs">
                  {dev.type}
                </Badge>
                {dev.submittedDate && (
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Calendar className="h-3 w-3" />
                    {new Date(dev.submittedDate).toLocaleDateString()}
                  </div>
                )}
              </div>
            </div>
          </div>
          <Badge variant={dev.status === "Approved" ? "default" : "outline"} className="ml-4 shrink-0">
            {dev.status}
          </Badge>
        </div>
      ))}
    </div>
  )
}
