import { useState } from "react"
import { TrendingUp, Home, DollarSign, ArrowUp, ArrowDown } from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import type { StreetRankingsData } from "@/types"

interface StreetRankingsTableProps {
  data: StreetRankingsData | null
  loading?: boolean
}

export function StreetRankingsTable({ data, loading }: StreetRankingsTableProps) {
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Street Rankings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12">
            <div className="text-muted-foreground">Loading street rankings...</div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!data || !data.summary || !data.priceRanking || !data.growthRanking || !data.rentRanking) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Street Rankings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12">
            <div className="text-muted-foreground">No street data available</div>
          </div>
        </CardContent>
      </Card>
    )
  }

  const toggleSort = () => {
    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
  }

  const getSortIcon = () => {
    if (sortOrder === 'asc') return <ArrowUp className="h-4 w-4" />
    return <ArrowDown className="h-4 w-4" />
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-chart-2" />
          Street Rankings & Analysis
        </CardTitle>
        <CardDescription>
          Detailed comparison of {data.summary.totalStreets} streets in this suburb
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="p-4 rounded-lg bg-primary/5 border border-primary/10">
            <div className="text-sm text-muted-foreground mb-1">Total Streets</div>
            <div className="text-2xl font-bold">{data.summary.totalStreets}</div>
          </div>
          <div className="p-4 rounded-lg bg-chart-2/5 border border-chart-2/10">
            <div className="text-sm text-muted-foreground mb-1">Avg Price</div>
            <div className="text-2xl font-bold">${(data.summary.avgPrice / 1000).toFixed(0)}k</div>
          </div>
          <div className="p-4 rounded-lg bg-chart-3/5 border border-chart-3/10">
            <div className="text-sm text-muted-foreground mb-1">Avg Growth</div>
            <div className="text-2xl font-bold">{data.summary.avgGrowth.toFixed(1)}%</div>
          </div>
          <div className="p-4 rounded-lg bg-chart-5/5 border border-chart-5/10">
            <div className="text-sm text-muted-foreground mb-1">Avg Rent</div>
            <div className="text-2xl font-bold">${data.summary.avgRent.toFixed(0)}</div>
          </div>
        </div>

        {/* Ranking Tables */}
        <Tabs defaultValue="price" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="price" className="flex items-center gap-2">
              <Home className="h-4 w-4" />
              Price Ranking
            </TabsTrigger>
            <TabsTrigger value="growth" className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              Growth Ranking
            </TabsTrigger>
            <TabsTrigger value="rent" className="flex items-center gap-2">
              <DollarSign className="h-4 w-4" />
              Rent Ranking
            </TabsTrigger>
          </TabsList>

          {/* Price Ranking Table */}
          <TabsContent value="price" className="mt-4">
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-16">Rank</TableHead>
                    <TableHead>Street Name</TableHead>
                    <TableHead className="text-right">
                      <button
                        onClick={toggleSort}
                        className="flex items-center gap-1 ml-auto hover:text-foreground"
                      >
                        Price {getSortIcon()}
                      </button>
                    </TableHead>
                    <TableHead className="text-right">Growth</TableHead>
                    <TableHead className="text-right">Properties</TableHead>
                    <TableHead>Market Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.priceRanking.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                        No data available
                      </TableCell>
                    </TableRow>
                  ) : (
                    data.priceRanking.map((street) => (
                      <TableRow key={street.rank}>
                        <TableCell className="font-medium">
                          <Badge variant={street.rank <= 3 ? "default" : "secondary"}>
                            #{street.rank}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-medium">{street.streetName}</TableCell>
                        <TableCell className="text-right font-semibold">
                          ${(street.price / 1000).toFixed(0)}k
                        </TableCell>
                        <TableCell className="text-right">
                          <span className={street.growth >= 0 ? "text-green-600" : "text-red-600"}>
                            {street.growth >= 0 ? "+" : ""}{street.growth.toFixed(1)}%
                          </span>
                        </TableCell>
                        <TableCell className="text-right">{street.properties}</TableCell>
                        <TableCell>
                          <Badge variant="outline" className="text-xs">
                            {street.turnoverComment}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </TabsContent>

          {/* Growth Ranking Table */}
          <TabsContent value="growth" className="mt-4">
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-16">Rank</TableHead>
                    <TableHead>Street Name</TableHead>
                    <TableHead className="text-right">
                      <button
                        onClick={toggleSort}
                        className="flex items-center gap-1 ml-auto hover:text-foreground"
                      >
                        Growth {getSortIcon()}
                      </button>
                    </TableHead>
                    <TableHead className="text-right">Price</TableHead>
                    <TableHead className="text-right">Properties</TableHead>
                    <TableHead className="text-right">Turnover</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.growthRanking.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                        No data available
                      </TableCell>
                    </TableRow>
                  ) : (
                    data.growthRanking.map((street) => (
                      <TableRow key={street.rank}>
                        <TableCell className="font-medium">
                          <Badge variant={street.rank <= 3 ? "default" : "secondary"}>
                            #{street.rank}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-medium">{street.streetName}</TableCell>
                        <TableCell className="text-right">
                          <div className="flex items-center justify-end gap-1">
                            {street.growth >= 0 ? (
                              <ArrowUp className="h-4 w-4 text-green-600" />
                            ) : (
                              <ArrowDown className="h-4 w-4 text-red-600" />
                            )}
                            <span className={`font-semibold ${street.growth >= 0 ? "text-green-600" : "text-red-600"}`}>
                              {street.growth >= 0 ? "+" : ""}{street.growth.toFixed(1)}%
                            </span>
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          ${(street.price / 1000).toFixed(0)}k
                        </TableCell>
                        <TableCell className="text-right">{street.properties}</TableCell>
                        <TableCell className="text-right">{street.turnoverRate.toFixed(1)}%</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </TabsContent>

          {/* Rent Ranking Table */}
          <TabsContent value="rent" className="mt-4">
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-16">Rank</TableHead>
                    <TableHead>Street Name</TableHead>
                    <TableHead className="text-right">
                      <button
                        onClick={toggleSort}
                        className="flex items-center gap-1 ml-auto hover:text-foreground"
                      >
                        Weekly Rent {getSortIcon()}
                      </button>
                    </TableHead>
                    <TableHead className="text-right">Price</TableHead>
                    <TableHead className="text-right">Rental Yield</TableHead>
                    <TableHead className="text-right">Renters %</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.rentRanking.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                        No data available
                      </TableCell>
                    </TableRow>
                  ) : (
                    data.rentRanking.map((street) => (
                      <TableRow key={street.rank}>
                        <TableCell className="font-medium">
                          <Badge variant={street.rank <= 3 ? "default" : "secondary"}>
                            #{street.rank}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-medium">{street.streetName}</TableCell>
                        <TableCell className="text-right font-semibold">
                          ${street.weeklyRent}/wk
                        </TableCell>
                        <TableCell className="text-right">
                          ${(street.price / 1000).toFixed(0)}k
                        </TableCell>
                        <TableCell className="text-right">
                          <span className="font-semibold text-chart-3">
                            {street.rentalYield.toFixed(2)}%
                          </span>
                        </TableCell>
                        <TableCell className="text-right">{street.rentersPercentage.toFixed(1)}%</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
