import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import type { AmenityCategory } from "@/types"

interface AmenitiesChartProps {
  data?: AmenityCategory[]
}

export function AmenitiesChart({ data }: AmenitiesChartProps) {
  // No fallback data - show empty state if no data
  if (!data || data.length === 0) {
    return (
      <div className="h-[300px] flex items-center justify-center text-muted-foreground">
        <div className="text-center">
          <p className="text-sm">No amenities data available</p>
          <p className="text-xs mt-1">Data will appear when loaded from API</p>
        </div>
      </div>
    )
  }

  const colors = [
    "var(--color-chart-6)",
    "var(--color-chart-1)",
    "var(--color-chart-5)",
    "var(--color-chart-7)",
    "var(--color-chart-2)",
    "var(--color-chart-4)",
  ]

  const formattedData = data.map((item, index) => ({
    category: item.name,
    count: item.count,
    fill: colors[index % colors.length],
  }))

  return (
    <ChartContainer
      config={{
        count: {
          label: "Count",
          color: "hsl(var(--chart-1))",
        },
      }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={formattedData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
          <XAxis type="number" className="text-xs" tick={{ fill: "hsl(var(--muted-foreground))" }} />
          <YAxis
            dataKey="category"
            type="category"
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
            width={80}
          />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Bar dataKey="count" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}
