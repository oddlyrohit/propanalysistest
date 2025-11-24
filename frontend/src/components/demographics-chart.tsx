import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import type { AgeDistribution } from "@/types"

interface DemographicsChartProps {
  data?: AgeDistribution[]
}

export function DemographicsChart({ data }: DemographicsChartProps) {
  // No fallback data - show empty state if no data
  if (!data || data.length === 0) {
    return (
      <div className="h-[300px] flex items-center justify-center text-muted-foreground">
        <div className="text-center">
          <p className="text-sm">No demographics data available</p>
          <p className="text-xs mt-1">Data will appear when loaded from API</p>
        </div>
      </div>
    )
  }

  const colors = [
    "var(--color-chart-1)",
    "var(--color-chart-2)",
    "var(--color-chart-3)",
    "var(--color-chart-4)",
    "var(--color-chart-5)",
    "var(--color-chart-6)",
    "var(--color-chart-7)",
  ]

  // Filter out "Total" and format the data
  const formattedData = data
    .filter((item) => item.age.toLowerCase() !== 'total')
    .map((item, index) => ({
      ...item,
      fill: colors[index % colors.length],
    }))

  return (
    <ChartContainer
      config={{
        percentage: {
          label: "Percentage",
          color: "hsl(var(--chart-1))",
        },
      }}
      className="h-[300px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
          <XAxis dataKey="age" className="text-xs" tick={{ fill: "hsl(var(--muted-foreground))" }} />
          <YAxis 
            className="text-xs" 
            tick={{ fill: "hsl(var(--muted-foreground))" }}
            label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }}
          />
          <ChartTooltip 
            content={<ChartTooltipContent />}
            formatter={(value: number) => [`${value}%`, 'Percentage']}
          />
          <Bar dataKey="percentage" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}

