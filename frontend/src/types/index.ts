export interface Suburb {
  id: string
  name: string
  state: string
  postcode: string
  population: number
  medianAge: number
  medianHousePrice: number
  medianRent: number
  amenitiesCount: number
  schoolsCount: number
  developmentApps: number
}

export interface AgeDistribution {
  age: string
  population: number
  percentage: number
}

export interface Ethnicity {
  name: string
  percentage: number
}

export interface Demographics {
  ageDistribution: AgeDistribution[]
  ethnicity: Ethnicity[]
}

export interface AmenityCategory {
  name: string
  count: number
  percentage: number
}

export interface Amenities {
  categories: AmenityCategory[]
  total: number
}

export interface PriceHistory {
  month: string
  price: number
}

export interface MarketTrends {
  priceHistory: PriceHistory[]
  quarterlyGrowth: number
  rentalYield: number
  daysOnMarket: number
}

// Real Microburbs API School Data (from real API)
export interface MicroburbsSchool {
  id: number
  name: string
  area_level: string
  area_name: string
  school_level_type: string  // "Primary", "Secondary", "Combined"
  school_sector_type: string // "Public", "Private", "Catholic"
  gender: string
  boys: number
  girls: number
  attendance_rate: number
  naplan: number             // 0-1 score
  naplan_rank: string        // "NAPLAN top 37%"
  socioeconomic: number      // 0-1 score
  socioeconomic_rank: string // "Affluence bottom 17%"
}

// Normalized School Data (for UI display - supports both formats)
export interface School {
  name: string
  type: string               // Primary, Secondary, Combined, Childcare
  sector: string             // Government, Catholic, Private, Independent
  rating?: number            // 0-5 rating (calculated or provided)
  distance?: number          // distance in km (if available)
  // Additional fields from real API
  naplanScore?: number       // NAPLAN score (0-1)
  naplanRank?: string        // NAPLAN rank text
  socioeconomicScore?: number // Socioeconomic score (0-1)
  socioeconomicRank?: string  // Socioeconomic rank text
  attendanceRate?: number     // Attendance rate (0-1)
  students?: {
    boys: number
    girls: number
    total: number
  }
}

export interface SchoolsData {
  schools: School[]
  total: number
}

// Helper function to convert Microburbs school data to normalized School format
export function normalizeSchool(school: MicroburbsSchool | School): School {
  // If it's already normalized, return as is
  if ('rating' in school || 'distance' in school) {
    return school as School
  }

  // Convert Microburbs format to normalized format
  const microburbsSchool = school as MicroburbsSchool
  const totalStudents = (microburbsSchool.boys || 0) + (microburbsSchool.girls || 0)

  return {
    name: microburbsSchool.name,
    type: microburbsSchool.school_level_type,
    sector: microburbsSchool.school_sector_type === 'Public' ? 'Government' : microburbsSchool.school_sector_type,
    rating: microburbsSchool.naplan ? Math.round(microburbsSchool.naplan * 5 * 10) / 10 : undefined, // Convert 0-1 to 0-5
    naplanScore: microburbsSchool.naplan,
    naplanRank: microburbsSchool.naplan_rank,
    socioeconomicScore: microburbsSchool.socioeconomic,
    socioeconomicRank: microburbsSchool.socioeconomic_rank,
    attendanceRate: microburbsSchool.attendance_rate,
    students: totalStudents > 0 ? {
      boys: microburbsSchool.boys || 0,
      girls: microburbsSchool.girls || 0,
      total: totalStudents
    } : undefined
  }
}

export interface Development {
  id: string
  name: string
  type: string
  status: string
  units: number
  address: string
  applicant: string
  submittedDate: string
}

export interface DevelopmentsData {
  developments: Development[]
  total: number
  showing: number
}

// Street Rankings Types
export interface StreetRanking {
  rank: number
  streetName: string
  price: number
  growth: number
  properties: number
  turnoverRate: number
  turnoverComment: string
}

export interface GrowthRanking {
  rank: number
  streetName: string
  growth: number
  price: number
  properties: number
  turnoverRate: number
}

export interface RentRanking {
  rank: number
  streetName: string
  weeklyRent: number
  price: number
  rentalYield: number
  properties: number
  rentersPercentage: number
}

export interface StreetRankingsData {
  priceRanking: StreetRanking[]
  growthRanking: GrowthRanking[]
  rentRanking: RentRanking[]
  summary: {
    totalStreets: number
    avgPrice: number
    avgGrowth: number
    avgRent: number
  }
}

// Street Insights Types (for raw API data)
export interface StreetInsightItem {
  area_level: string
  area_name: string
  growth: number
  properties: number
  property_type: string
  renters_percentage: number
  street_type: string
  turnover_rate: {
    comment: string
    value: number
  }
  turnover_rate_rent: {
    comment: string
    value: number
  }
  value: number
  value_rent: number
}

export interface StreetInsights {
  results: StreetInsightItem[]
}
