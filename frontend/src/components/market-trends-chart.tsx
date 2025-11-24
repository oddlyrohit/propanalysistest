import { CartesianGrid, XAxis, YAxis, ResponsiveContainer, Area, AreaChart } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import type { PriceHistory } from "@/types"
import { useMemo } from "react"

interface MarketTrendsChartProps {
  data?: PriceHistory[]
}

export function MarketTrendsChart({ data }: MarketTrendsChartProps) {
  // Transform API data to chart format
  const chartData = useMemo(() => {
    if (!data || data.length === 0) return []

    // API returns { date, suburb, cr, sa3 } but we expect { month, price }
    // Check if data needs transformation
    const firstItem = data[0] as any

    if ('date' in firstItem && 'suburb' in firstItem) {
      // Transform API format to chart format
      return data.map((item: any) => ({
        month: new Date(item.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short' }),
        price: item.suburb,
        cr: item.cr,
        sa3: item.sa3
      }))
    }

    // Data is already in correct format
    return data
  }, [data])

  // No fallback data - show empty state if no data
  if (!chartData || chartData.length === 0) {
    return (
      <div className="h-[450px] flex items-center justify-center text-muted-foreground">
        <div className="text-center">
          <p className="text-sm">No market trends data available</p>
          <p className="text-xs mt-1">Data will appear when loaded from API</p>
        </div>
      </div>
    )
  }

  return (
    <ChartContainer
      config={{
        price: {
          label: "Suburb Price",
          color: "hsl(var(--chart-2))",
        },
        cr: {
          label: "CR Average",
          color: "hsl(var(--chart-3))",
        },
        sa3: {
          label: "SA3 Average",
          color: "hsl(var(--chart-4))",
        },
      }}
      className="h-[450px]"
    >
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="var(--color-chart-2)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="var(--color-chart-2)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
          <XAxis
            dataKey="month"
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
            interval="preserveStartEnd"
            tickFormatter={(value) => {
              // Show every 24th tick (roughly yearly)
              return value
            }}
          />
          <YAxis
            className="text-xs"
            tick={{ fill: "hsl(var(--muted-foreground))" }}
            tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
          />
          <ChartTooltip
            content={<ChartTooltipContent />}
            formatter={(value: number, name: string) => {
              const label = name === 'price' ? 'Suburb' : name === 'cr' ? 'CR Avg' : 'SA3 Avg'
              return [`$${value.toLocaleString()}`, label]
            }}
          />
          <Area
            type="monotone"
            dataKey="price"
            stroke="var(--color-chart-2)"
            strokeWidth={2}
            fill="url(#colorPrice)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartContainer>
  )
}
