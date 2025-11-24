import { MapPin } from "lucide-react"

interface SuburbMapProps {
  suburb?: string
}

export function SuburbMap({ suburb }: SuburbMapProps) {
  return (
    <div className="h-[400px] w-full rounded-lg border border-border bg-muted/30 flex flex-col items-center justify-center">
      <MapPin className="h-12 w-12 text-muted-foreground mb-4" />
      <p className="text-muted-foreground text-center">
        Map view for {suburb || "selected suburb"}
        <br />
        <span className="text-sm">(Map integration coming soon)</span>
      </p>
    </div>
  )
}

