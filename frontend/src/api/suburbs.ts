import { fetchApi } from './client'
import type {
  Suburb,
  Demographics,
  Amenities,
  MarketTrends,
  SchoolsData,
  DevelopmentsData,
  MicroburbsSchool,
  School,
  StreetInsights,
  StreetRankingsData,
  SuburbSummary,
  SuburbInfo,
} from '../types'
import { normalizeSchool } from '../types'

export async function searchSuburbs(query: string): Promise<Suburb[]> {
  return fetchApi<Suburb[]>(`/api/suburbs/search?q=${encodeURIComponent(query)}`)
}

export async function getSuburb(suburbId: string): Promise<Suburb> {
  return fetchApi<Suburb>(`/api/suburb/${suburbId}`)
}

export async function getSuburbInfo(suburbId: string): Promise<SuburbInfo> {
  return fetchApi<SuburbInfo>(`/api/suburb/${suburbId}/info?geojson=true`)
}

export async function getDemographics(suburbId: string): Promise<Demographics> {
  const response = await fetchApi<Record<string, Demographics>>(
    `/api/suburb/${suburbId}/demographics`
  )
  // Extract data from suburb_id wrapper - throw error if not found
  const data = response[suburbId]
  if (!data) {
    throw new Error(`Demographics data not found for suburb: ${suburbId}`)
  }
  return data
}

export async function getAmenities(suburbId: string): Promise<Amenities> {
  const response = await fetchApi<Record<string, Amenities>>(
    `/api/suburb/${suburbId}/amenities`
  )
  // Extract data from suburb_id wrapper - throw error if not found
  const data = response[suburbId]
  if (!data) {
    throw new Error(`Amenities data not found for suburb: ${suburbId}`)
  }
  return data
}

export async function getMarketTrends(suburbId: string): Promise<MarketTrends> {
  const response = await fetchApi<Record<string, MarketTrends>>(
    `/api/suburb/${suburbId}/market-trends`
  )
  // Extract data from suburb_id wrapper - throw error if not found
  const data = response[suburbId]
  if (!data) {
    throw new Error(`Market trends data not found for suburb: ${suburbId}`)
  }
  return data
}

export async function getSchools(suburbId: string): Promise<SchoolsData> {
  // Backend may return either MicroburbsSchool[] or School[] format
  interface RawSchoolsData {
    schools: (MicroburbsSchool | School)[]
    total: number
  }

  const response = await fetchApi<Record<string, RawSchoolsData>>(
    `/api/suburb/${suburbId}/schools`
  )

  const rawData = response[suburbId]
  if (!rawData) {
    throw new Error(`Schools data not found for suburb: ${suburbId}`)
  }

  // Normalize all schools to the unified School format
  const normalizedSchools = rawData.schools.map(normalizeSchool)

  return {
    schools: normalizedSchools,
    total: rawData.total
  }
}

export async function getDevelopments(suburbId: string): Promise<DevelopmentsData> {
  const response = await fetchApi<Record<string, DevelopmentsData>>(
    `/api/suburb/${suburbId}/developments`
  )
  // Extract data from suburb_id wrapper - throw error if not found
  const data = response[suburbId]
  if (!data) {
    throw new Error(`Developments data not found for suburb: ${suburbId}`)
  }
  return data
}

export async function getStreetInsights(suburbId: string): Promise<StreetInsights> {
  const response = await fetchApi<Record<string, StreetInsights>>(
    `/api/suburb/${suburbId}/street-insights?geojson=false`
  )
  // Extract data from suburb_id wrapper - throw error if not found
  const data = response[suburbId]
  if (!data) {
    throw new Error(`Street insights data not found for suburb: ${suburbId}`)
  }
  return data
}

export async function getStreetRankings(suburbId: string, propertyType?: string): Promise<StreetRankingsData> {
  const params = new URLSearchParams()
  if (propertyType) {
    params.append('property_type', propertyType)
  }

  const endpoint = `/api/suburbs/${suburbId}/street-rankings${params.toString() ? '?' + params.toString() : ''}`
  return fetchApi<StreetRankingsData>(endpoint)
}

export async function getSuburbSummary(suburbId: string): Promise<SuburbSummary> {
  const response = await fetchApi<Record<string, SuburbSummary>>(
    `/api/suburb/${suburbId}/summary`
  )
  // Extract data from suburb_id wrapper - throw error if not found
  const data = response[suburbId]
  if (!data) {
    throw new Error(`Summary data not found for suburb: ${suburbId}`)
  }
  return data
}
