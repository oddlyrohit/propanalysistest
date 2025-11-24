import { Bar, BarChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import type { Ethnicity } from "@/types"

interface EthnicityChartProps {
  data?: Ethnicity[]
}

export function EthnicityChart({ data }: EthnicityChartProps) {
  // No fallback data - show empty state if no data
  if (!data || data.length === 0) {
    return (
      <div className="h-[400px] flex items-center justify-center text-muted-foreground">
        <div className="text-center">
          <p className="text-sm">No ethnicity data available</p>
          <p className="text-xs mt-1">Data will appear when loaded from API</p>
        </div>
      </div>
    )
  }

  // Take top 8 ethnicities and sort by percentage descending
  const topEthnicities = [...data]
    .sort((a, b) => b.percentage - a.percentage)
    .slice(0, 8)
    .map((item) => ({
      name: item.name,
      percentage: item.percentage,
    }))

  return (
    <ChartContainer
      config={{
        percentage: {
          label: "Percentage",
          color: "hsl(var(--chart-2))",
        },
      }}
      className="h-[400px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={topEthnicities}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" horizontal={false} />
          <XAxis
            type="number"
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
            tickFormatter={(value) => `${value}%`}
          />
          <YAxis
            type="category"
            dataKey="name"
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
            width={180}
          />
          <ChartTooltip
            content={<ChartTooltipContent />}
            formatter={(value: number) => [`${value.toFixed(1)}%`, "Percentage"]}
          />
          <Bar
            dataKey="percentage"
            fill="var(--color-chart-2)"
            radius={[0, 4, 4, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}
