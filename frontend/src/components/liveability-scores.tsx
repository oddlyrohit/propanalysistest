import { Card, CardContent } from "@/components/ui/card"
import { Info, Lock } from "lucide-react"
import type { SummaryScore, GeoJSON } from "@/types"
import { useEffect, useRef } from "react"
import 'leaflet/dist/leaflet.css'

interface LiveabilityScoresProps {
  scores?: SummaryScore[]
  geometry?: GeoJSON
  suburbName?: string
}

interface ScoreCardProps {
  icon: string
  title: string
  value: string
}

function ScoreCard({ icon, title, value }: ScoreCardProps) {
  return (
    <Card className="border-border">
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="text-xl">{icon}</div>
          <Info className="h-4 w-4 text-muted-foreground cursor-help" />
        </div>
        <div className="space-y-1">
          <div className="text-xs font-medium text-muted-foreground">
            {title}
          </div>
          <div className="text-xl font-bold text-foreground">
            {value}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function SuburbBoundaryMap({ geometry, suburbName }: { geometry?: GeoJSON; suburbName?: string }) {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<any>(null)

  useEffect(() => {
    if (!mapRef.current || !geometry || typeof window === 'undefined') return

    // Dynamically import Leaflet
    import('leaflet').then((L) => {
      if (!mapRef.current) return

      // Clean up existing map
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }

      // Create map
      const map = L.map(mapRef.current, {
        zoomControl: true,
        scrollWheelZoom: false,
      })

      mapInstanceRef.current = map

      // Add CartoDB map tiles (works better in China)
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a> | <a href="https://www.microburbs.com.au">Microburbs</a>',
        maxZoom: 19,
        subdomains: 'abcd'
      }).addTo(map)

      // Add GeoJSON boundary
      const geoJsonLayer = L.geoJSON({
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Polygon',
          coordinates: geometry.coordinates,
        }
      } as any, {
        style: {
          color: '#3b82f6',
          weight: 3,
          opacity: 0.8,
          fillColor: '#3b82f6',
          fillOpacity: 0.1,
        },
      }).addTo(map)

      // Fit map to bounds
      map.fitBounds(geoJsonLayer.getBounds())
    }).catch((error) => {
      console.error('Failed to load Leaflet:', error)
    })

    // Cleanup on unmount
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [geometry, suburbName])

  if (!geometry) {
    return (
      <div className="h-[280px] bg-muted rounded-lg flex items-center justify-center">
        <p className="text-sm text-muted-foreground">Map loading...</p>
      </div>
    )
  }

  return <div ref={mapRef} className="h-[280px] rounded-lg border border-border z-0" />
}

export function LiveabilityScores({ scores, geometry, suburbName }: LiveabilityScoresProps) {
  if (!scores || scores.length === 0) {
    return null
  }

  // Extract specific scores for display
  const getScore = (id: string) => scores.find(s => s.id === id)

  const lifestyleScore = getScore('lifestyle-score')
  const tranquillityScore = getScore('tranquility-score') // Note: API uses 'tranquility' (US spelling)
  const hipScore = getScore('hip-score')
  const safetyScore = getScore('safety-score')

  return (
    <>
      {/* Map */}
      <div className="mb-4">
        <SuburbBoundaryMap geometry={geometry} suburbName={suburbName} />
      </div>

      {/* Liveability Section */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <h3 className="text-lg font-semibold">Liveability</h3>
          <Info className="h-4 w-4 text-muted-foreground cursor-help" />
        </div>
        <p className="text-sm text-muted-foreground">
          Discover how different factors, such as climate, tranquillity, and safety,
          influence livability in {suburbName || 'this suburb'}.
        </p>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        {lifestyleScore && (
          <ScoreCard
            icon="🏃"
            title="Lifestyle Score"
            value={lifestyleScore.value}
          />
        )}
        {tranquillityScore && (
          <ScoreCard
            icon="💆"
            title="Tranquillity Score"
            value={tranquillityScore.value}
          />
        )}
        {hipScore && (
          <ScoreCard
            icon="😎"
            title="Hip Score"
            value={hipScore.value}
          />
        )}
        {safetyScore && (
          <ScoreCard
            icon="🏫"
            title="Safety Score"
            value={safetyScore.value}
          />
        )}
      </div>

      {/* Marketing Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 border-2 border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
              You are seeing a partial report
            </p>
          </div>
          <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors flex items-center gap-2 shadow-sm">
            <Lock className="h-4 w-4" />
            Unlock Full Report
          </button>
        </div>
      </div>
    </>
  )
}

