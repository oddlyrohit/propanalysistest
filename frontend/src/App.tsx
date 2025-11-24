import { useState } from "react"
import { Search, MapPin, TrendingUp, Users, Building2, School, Home, AlertCircle, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { DemographicsChart } from "@/components/demographics-chart"
import { EthnicityChart } from "@/components/ethnicity-chart"
import { AmenitiesChart } from "@/components/amenities-chart"
import { MarketTrendsChart } from "@/components/market-trends-chart"
import { SchoolsList } from "@/components/schools-list"
import { DevelopmentList } from "@/components/development-list"
import { SuburbMap } from "@/components/suburb-map"
import { MicroburbsLogo } from "@/components/microburbs-logo"
import { StreetRankingsTable } from "@/components/street-rankings-table"
import { LiveabilityScores } from "@/components/liveability-scores"
import * as SuburbsApi from "@/api/suburbs"
import type { Suburb, Demographics, Amenities, MarketTrends, SchoolsData, DevelopmentsData, StreetRankingsData, SuburbSummary, SuburbInfo } from "@/types"

function App() {
  const [suburb, setSuburb] = useState<Suburb | null>(null)
  const [searchInput, setSearchInput] = useState("")
  const [hasSearched, setHasSearched] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Data states
  const [demographics, setDemographics] = useState<Demographics | null>(null)
  const [amenities, setAmenities] = useState<Amenities | null>(null)
  const [marketTrends, setMarketTrends] = useState<MarketTrends | null>(null)
  const [schools, setSchools] = useState<SchoolsData | null>(null)
  const [developments, setDevelopments] = useState<DevelopmentsData | null>(null)
  const [streetRankings, setStreetRankings] = useState<StreetRankingsData | null>(null)
  const [summary, setSummary] = useState<SuburbSummary | null>(null)
  const [suburbInfo, setSuburbInfo] = useState<SuburbInfo | null>(null)

  const handleSearch = async () => {
    if (!searchInput.trim()) return

    setLoading(true)
    setError(null)

    try {
      // Search for suburbs
      const results = await SuburbsApi.searchSuburbs(searchInput)
      
      if (results.length === 0) {
        setError("No suburbs found. Try 'Melbourne', 'Sydney', or 'Brisbane'")
        setLoading(false)
        return
      }

      // Get the first result
      const firstResult = results[0]
      setSuburb(firstResult)
      setHasSearched(true)

      // Fetch all related data
      await Promise.all([
        fetchDemographics(firstResult.id),
        fetchAmenities(firstResult.id),
        fetchMarketTrends(firstResult.id),
        fetchSchools(firstResult.id),
        fetchDevelopments(firstResult.id),
        fetchStreetRankings(firstResult.id),
        fetchSummary(firstResult.id),
        fetchSuburbInfo(firstResult.id),
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch data")
    } finally {
      setLoading(false)
    }
  }

  const fetchDemographics = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getDemographics(suburbId)
      setDemographics(data)
    } catch (err) {
      console.error("Failed to fetch demographics:", err)
    }
  }

  const fetchAmenities = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getAmenities(suburbId)
      setAmenities(data)
    } catch (err) {
      console.error("Failed to fetch amenities:", err)
    }
  }

  const fetchMarketTrends = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getMarketTrends(suburbId)
      setMarketTrends(data)
    } catch (err) {
      console.error("Failed to fetch market trends:", err)
    }
  }

  const fetchSchools = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getSchools(suburbId)
      setSchools(data)
    } catch (err) {
      console.error("Failed to fetch schools:", err)
    }
  }

  const fetchDevelopments = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getDevelopments(suburbId)
      setDevelopments(data)
    } catch (err) {
      console.error("Failed to fetch developments:", err)
    }
  }

  const fetchStreetRankings = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getStreetRankings(suburbId, 'house')
      setStreetRankings(data)
    } catch (err) {
      console.error("Failed to fetch street rankings:", err)
    }
  }

  const fetchSummary = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getSuburbSummary(suburbId)
      setSummary(data)
    } catch (err) {
      console.error("Failed to fetch summary:", err)
    }
  }

  const fetchSuburbInfo = async (suburbId: string) => {
    try {
      const data = await SuburbsApi.getSuburbInfo(suburbId)
      setSuburbInfo(data)
    } catch (err) {
      console.error("Failed to fetch suburb info:", err)
    }
  }

  const handleLogoClick = () => {
    setSuburb(null)
    setSearchInput("")
    setHasSearched(false)
    setError(null)
    setDemographics(null)
    setAmenities(null)
    setMarketTrends(null)
    setSchools(null)
    setDevelopments(null)
    setStreetRankings(null)
    setSummary(null)
    setSuburbInfo(null)
  }

  const handleExampleClick = (example: string) => {
    setSearchInput(example)
    setTimeout(() => {
      handleSearch()
    }, 100)
  }

  if (!hasSearched) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <header className="py-4">
          <div className="container mx-auto px-4">
            <button onClick={handleLogoClick} className="hover:opacity-75 transition-opacity">
              <MicroburbsLogo size="lg" />
            </button>
          </div>
        </header>

        <main className="flex-1 flex items-center justify-center px-4">
          <div className="w-full max-w-3xl -mt-24">
            <div className="text-center mb-12">
              <div className="mb-8">
                <MicroburbsLogo size="xl" textSize="text-5xl font-normal" />
              </div>
            </div>

            <div className="bg-background border border-border shadow-lg rounded-full hover:shadow-xl transition-shadow">
              <div className="flex items-center gap-3 px-6 py-4">
                <Search className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                <Input
                  type="text"
                  placeholder="Search suburb, postcode or address"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  className="border-0 text-lg h-auto p-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent placeholder:text-muted-foreground/60"
                  disabled={loading}
                />
                {searchInput && (
                  <Button
                    onClick={handleSearch}
                    size="sm"
                    className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-full px-6"
                    disabled={loading}
                  >
                    {loading ? "Searching..." : "Search"}
                  </Button>
                )}
              </div>
            </div>

            {error && (
              <div className="mt-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm flex items-center justify-center gap-2">
                <AlertCircle className="h-4 w-4" />
                <span>{error}</span>
              </div>
            )}

            <div className="mt-10 flex flex-wrap gap-3 justify-center items-center text-sm text-muted-foreground">
              <span>Try:</span>
              {["Belmont North", "Sydney CBD", "Brisbane City", "Perth"].map((example) => (
                <button
                  key={example}
                  onClick={() => handleExampleClick(example)}
                  className="text-primary hover:underline"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </main>

        <footer className="py-4">
          <div className="container mx-auto px-4 text-center text-xs text-muted-foreground space-y-1">
            <p>Australian Suburb Analysis Platform</p>
            <p className="text-muted-foreground/60">Powered by Microburbs</p>
          </div>
        </footer>
      </div>
    )
  }

  if (!suburb) return null

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card sticky top-0 z-40">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center gap-6">
            <button onClick={handleLogoClick} className="hover:opacity-75 transition-opacity flex-shrink-0">
              <MicroburbsLogo size="md" />
            </button>

            <div className="flex-1 max-w-2xl">
              <div className="bg-background border border-border rounded-full hover:border-primary/50 transition-colors">
                <div className="flex items-center gap-2 px-4 py-2">
                  <Search className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <Input
                    type="text"
                    placeholder="Search another location..."
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                    className="border-0 text-sm h-auto p-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent"
                    disabled={loading}
                  />
                  {searchInput && (
                    <Button 
                      onClick={handleSearch}
                      size="sm"
                      className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-full h-7 px-4 text-xs"
                      disabled={loading}
                    >
                      {loading ? "Loading..." : "Search"}
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Overview */}
      <section className="border-b border-border bg-secondary/30">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center gap-2 mb-6">
            <MapPin className="h-5 w-5 text-primary" />
            <h2 className="text-2xl font-semibold text-foreground">
              {suburb.name}, {suburb.state} {suburb.postcode}
            </h2>
          </div>

          {/* Liveability and Market Data Section */}
          <Card className="border-border bg-white">
            <CardContent className="p-5">
              <div className="grid lg:grid-cols-3 gap-4">
                {/* Left: Liveability Section - Takes 2 columns */}
                <div className="lg:col-span-2">
                  <LiveabilityScores
                    scores={summary?.results}
                    geometry={suburbInfo?.geometry}
                    suburbName={suburb.name}
                  />
                </div>

                {/* Right: Market Data Cards - Takes 1 column */}
                <div className="flex flex-col gap-3 h-full">
                  {/* Median House Price */}
                  <Card className="bg-card border-border hover:shadow-lg transition-shadow flex-1 flex flex-col">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-xs flex items-center gap-2 text-muted-foreground font-medium">
                        <Home className="h-4 w-4" />
                        Median House Price
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 flex flex-col justify-center">
                      <div className="text-xl font-bold">
                        ${marketTrends?.currentPrice ? marketTrends.currentPrice.toLocaleString() : suburb.medianHousePrice.toLocaleString()}
                      </div>
                      {marketTrends?.priceGrowth && (
                        <div className="flex items-center gap-1 mt-1 text-xs text-green-600 dark:text-green-400">
                          <TrendingUp className="h-3 w-3" />
                          <span>+{marketTrends.priceGrowth['1year'].toFixed(1)}%</span>
                        </div>
                      )}
                    </CardContent>
                  </Card>

                  {/* Rental Yield */}
                  <Card className="bg-card border-border hover:shadow-lg transition-shadow flex-1 flex flex-col">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-xs flex items-center gap-2 text-muted-foreground font-medium">
                        <TrendingUp className="h-4 w-4" />
                        Rental Yield
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 flex flex-col justify-center">
                      <div className="text-xl font-bold">
                        {marketTrends?.rentalYield ? marketTrends.rentalYield.toFixed(1) : '3.4'}%
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">Annual ROI</p>
                    </CardContent>
                  </Card>

                  {/* Days on Market */}
                  <Card className="bg-card border-border hover:shadow-lg transition-shadow flex-1 flex flex-col">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-xs flex items-center gap-2 text-muted-foreground font-medium">
                        <Clock className="h-4 w-4" />
                        Days on Market
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 flex flex-col justify-center">
                      <div className="text-xl font-bold">
                        {marketTrends?.daysOnMarket || '42'}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">Avg. days to sell</p>
                    </CardContent>
                  </Card>

                  {/* Total Amenities */}
                  <Card className="bg-card border-border hover:shadow-lg transition-shadow flex-1 flex flex-col">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-xs flex items-center gap-2 text-muted-foreground font-medium">
                        <MapPin className="h-4 w-4" />
                        Total Amenities
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 flex flex-col justify-center">
                      <div className="text-xl font-bold">
                        {amenities?.total || '153'}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">Nearby facilities</p>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Main Content */}
      <section className="container mx-auto px-4 py-8">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 lg:w-auto lg:inline-grid bg-muted">
            <TabsTrigger value="overview" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">Overview</TabsTrigger>
            <TabsTrigger value="demographics" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">Demographics</TabsTrigger>
            <TabsTrigger value="amenities" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">Amenities</TabsTrigger>
            <TabsTrigger value="market" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">Market Data</TabsTrigger>
            <TabsTrigger value="development" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">Development</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {!summary?.results || summary.results.length === 0 ? (
              <Card className="bg-card border-border">
                <CardContent className="p-12 text-center">
                  <p className="text-muted-foreground">Loading suburb summary...</p>
                </CardContent>
              </Card>
            ) : (
              <div className="grid lg:grid-cols-2 gap-6">
                {summary.results.map((score) => (
                  <Card key={score.id} className="bg-card border-border">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <CardTitle className="flex items-center gap-2 text-lg">
                            {score.name}
                          </CardTitle>
                          <CardDescription className="mt-1">
                            {score.area_level}: {score.area_name}
                          </CardDescription>
                        </div>
                        <div className="text-2xl font-bold text-chart-2">
                          {score.value}
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {/* Comment */}
                      {score.comment && (
                        <div className="p-3 rounded-lg bg-primary/5 border border-primary/10">
                          <p className="text-sm text-foreground">{score.comment}</p>
                        </div>
                      )}

                      {/* Adjectives */}
                      {score.adjectives && score.adjectives.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {score.adjectives.map((adj, idx) => (
                            <span
                              key={idx}
                              className="px-3 py-1 text-xs font-medium rounded-full bg-chart-2/10 text-chart-2 border border-chart-2/20"
                            >
                              {adj}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Summary Points */}
                      {score.summary && score.summary.length > 0 && (
                        <div className="space-y-2">
                          {score.summary.map((point, idx) => (
                            <div key={idx} className="flex items-start gap-2">
                              <div className="h-1.5 w-1.5 rounded-full bg-chart-2 mt-2 flex-shrink-0" />
                              <p className="text-sm text-muted-foreground flex-1">{point}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="demographics" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              <Card className="bg-card border-border">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5 text-chart-1" />
                    Age Distribution
                  </CardTitle>
                  <CardDescription>Population breakdown by age group</CardDescription>
                </CardHeader>
                <CardContent>
                  <DemographicsChart data={demographics?.ageDistribution} />
                </CardContent>
              </Card>

              <Card className="bg-card border-border">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5 text-chart-4" />
                    Cultural Background
                  </CardTitle>
                  <CardDescription>Top 10 ethnicities in the area</CardDescription>
                </CardHeader>
                <CardContent>
                  <EthnicityChart data={demographics?.ethnicity} />
                </CardContent>
              </Card>
            </div>

            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-primary" />
                  Demographic Insights
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start gap-3 p-4 rounded-lg bg-primary/5 border border-primary/10">
                  <AlertCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold mb-1">Family-Friendly Area</h4>
                    <p className="text-sm text-muted-foreground">
                      High proportion of families with children, excellent schools nearby
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-4 rounded-lg bg-accent/5 border border-accent/10">
                  <AlertCircle className="h-5 w-5 text-accent mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold mb-1">Diverse Community</h4>
                    <p className="text-sm text-muted-foreground">
                      Multicultural neighborhood with various cultural amenities
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="amenities" className="space-y-6">
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Building2 className="h-5 w-5 text-chart-5" />
                  Amenities Overview
                </CardTitle>
                <CardDescription>Distribution of facilities in {suburb.name}</CardDescription>
              </CardHeader>
              <CardContent>
                <AmenitiesChart data={amenities?.categories} />
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <School className="h-5 w-5 text-chart-5" />
                  Schools & Education
                </CardTitle>
                <CardDescription>
                  {schools ? `${schools.total} schools in the area` : 'Loading schools data...'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <SchoolsList schools={schools?.schools} />
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-primary" />
                  Location Map
                </CardTitle>
                <CardDescription>View all amenities on the map</CardDescription>
              </CardHeader>
              <CardContent>
                <SuburbMap suburb={suburb.name} />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="market" className="space-y-6">
            {/* Price Trends Section - Chart on left (75%), Stats on right (25%) */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Price Trends Chart - Takes 3 columns (75%) */}
              <div className="md:col-span-3">
                <Card className="bg-card border-border h-full">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-chart-2" />
                      Price Trends
                    </CardTitle>
                    <CardDescription>Historical price data and forecasts</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <MarketTrendsChart data={marketTrends?.priceHistory} />
                  </CardContent>
                </Card>
              </div>

              {/* Market Statistics - Takes 1 column (25%), 3 Cards Stacked */}
              <div className="md:col-span-1 flex flex-col gap-4">
                <Card className="bg-card/80 backdrop-blur-sm border-l-4 border-l-chart-2 hover:shadow-lg hover:shadow-chart-2/10 transition-all duration-300">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base flex items-center gap-2">
                      <Home className="h-4 w-4 text-chart-2" />
                      Median House Price
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold bg-gradient-to-r from-foreground to-chart-2 bg-clip-text">
                      ${marketTrends?.currentPrice ? marketTrends.currentPrice.toLocaleString() : suburb.medianHousePrice.toLocaleString()}
                    </div>
                    {marketTrends?.priceGrowth && (
                      <div className="flex items-center gap-1 mt-2 text-sm text-green-600 dark:text-green-400">
                        <TrendingUp className="h-4 w-4" />
                        <span>+{marketTrends.priceGrowth['1year'].toFixed(1)}% this year</span>
                      </div>
                    )}
                  </CardContent>
                </Card>

                <Card className="bg-card/80 backdrop-blur-sm border-l-4 border-l-chart-3 hover:shadow-lg hover:shadow-chart-3/10 transition-all duration-300">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-chart-3" />
                      Rental Yield
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold bg-gradient-to-r from-foreground to-chart-3 bg-clip-text">
                      {marketTrends?.rentalYield ? marketTrends.rentalYield.toFixed(1) : '3.4'}%
                    </div>
                    <p className="text-sm text-muted-foreground mt-2">${suburb.medianRent}/week median rent</p>
                  </CardContent>
                </Card>

                <Card className="bg-card/80 backdrop-blur-sm border-l-4 border-l-chart-6 hover:shadow-lg hover:shadow-chart-6/10 transition-all duration-300">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-chart-6" />
                      Days on Market
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold bg-gradient-to-r from-foreground to-chart-6 bg-clip-text">
                      {marketTrends?.daysOnMarket || 32}
                    </div>
                    <p className="text-sm text-muted-foreground mt-2">Average selling time</p>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Street Rankings Table */}
            <StreetRankingsTable
              data={streetRankings}
              loading={loading}
            />
          </TabsContent>

          <TabsContent value="development" className="space-y-6">
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Building2 className="h-5 w-5 text-chart-7" />
                  Recent Development Applications
                </CardTitle>
                <CardDescription>
                  {developments?.total || 0} applications in the past 12 months
                </CardDescription>
              </CardHeader>
              <CardContent>
                <DevelopmentList developments={developments?.developments} />
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-primary" />
                  Development Map
                </CardTitle>
                <CardDescription>View development locations</CardDescription>
              </CardHeader>
              <CardContent>
                <SuburbMap suburb={suburb.name} />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/50 backdrop-blur-sm mt-12">
        <div className="container mx-auto px-4 py-10">
          <div className="text-center text-sm text-muted-foreground">
            <p className="font-medium">Street-level property data analysis • Updated weekly</p>
            <p className="mt-3 text-xs">Built with Flask + React + Vite</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
