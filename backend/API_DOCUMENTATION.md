# Backend API Documentation

## Overview

This document describes all available API endpoints for the Real Estate Property Analysis application backend.

### Base URL

```
http://localhost:5001
```

### Authentication

No authentication is currently required for any endpoints.

### Response Format

All endpoints return JSON responses with appropriate HTTP status codes:

- `200 OK` - Request successful
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error occurred

### Data Sources

The API uses a smart fallback mechanism:

- **NSW Suburbs** (e.g., Belmont North): Real-time data from Microburbs API
- **Other Suburbs** (e.g., Melbourne, Sydney, Brisbane): High-quality static fallback data

This ensures 100% uptime and consistent user experience regardless of external API availability.

---

## Core Endpoints

### 1. Search Suburbs

Search for suburbs by name.

**Endpoint:**
```
GET /api/suburbs/search
```

**Query Parameters:**

| Parameter | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| q         | string | Yes      | Search query (suburb name) |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburbs/search?q=mel"
```

**Success Response (200 OK):**
```json
[
  {
    "id": "",
    "name": "",
    "state": "",
    "postcode": "",
    "population": 0,
    "median_price": 0
  }
]
```

**Response Fields:**

| Field         | Type   | Description                    |
|---------------|--------|--------------------------------|
| id            | string | Suburb identifier              |
| name          | string | Suburb name                    |
| state         | string | Australian state abbreviation  |
| postcode      | string | Postal code                    |
| population    | number | Population count               |
| median_price  | number | Median property price in AUD   |

**Data Source:** Real API for all suburbs

---

### 2. Get Suburb Details

Get detailed information about a specific suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier (e.g., "melbourne-3000") |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/melbourne-3000"
```

**Success Response (200 OK):**
```json
{
  "id": "melbourne-3000",
  "name": "Melbourne",
  "state": "VIC",
  "postcode": "3000",
  "population": 8542,
  "medianAge": 38,
  "medianHousePrice": 785000,
  "medianRent": 520,
  "amenitiesCount": 127,
  "schoolsCount": 8,
  "developmentApps": 23
}
```

**Response Fields:**

| Field            | Type   | Description                           |
|------------------|--------|---------------------------------------|
| id               | string | Suburb identifier                     |
| name             | string | Suburb name                           |
| state            | string | Australian state abbreviation         |
| postcode         | string | Postal code                           |
| population       | number | Population count                      |
| medianAge        | number | Median age of residents               |
| medianHousePrice | number | Median house price in AUD             |
| medianRent       | number | Median weekly rent in AUD             |
| amenitiesCount   | number | Total number of nearby amenities      |
| schoolsCount     | number | Total number of nearby schools        |
| developmentApps  | number | Number of development applications    |

**Error Responses:**
- `404 Not Found` - Suburb not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API (NSW) / Fallback (others)

---

### 3. Get Demographics

Get demographic data for a suburb including age distribution and ethnicity.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/demographics
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/melbourne-3000/demographics"
```

**Success Response (200 OK):**
```json
{
  "melbourne-3000": {
    "ageDistribution": [
      {
        "age": "0-14",
        "population": 1245,
        "percentage": 14.6
      },
      {
        "age": "15-24",
        "population": 892,
        "percentage": 10.4
      },
      {
        "age": "25-34",
        "population": 1567,
        "percentage": 18.3
      }
    ],
    "ethnicity": [
      {
        "name": "Australian",
        "percentage": 28.5
      },
      {
        "name": "English",
        "percentage": 18.2
      },
      {
        "name": "Chinese",
        "percentage": 12.4
      }
    ]
  }
}
```

**Response Structure:**

The response is keyed by suburb ID and contains:

**ageDistribution** (array):
| Field      | Type   | Description                    |
|------------|--------|--------------------------------|
| age        | string | Age range                      |
| population | number | Population count in this range |
| percentage | number | Percentage of total population |

**ethnicity** (array):
| Field      | Type   | Description                    |
|------------|--------|--------------------------------|
| name       | string | Ethnicity name                 |
| percentage | number | Percentage of total population |

**Error Responses:**
- `404 Not Found` - Demographics not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API (NSW) / Fallback (others)

---

### 4. Get Amenities

Get information about nearby amenities including restaurants, cafes, parks, etc.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/amenities
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/melbourne-3000/amenities"
```

**Success Response (200 OK):**
```json
{
  "melbourne-3000": {
    "categories": [
      {
        "name": "Restaurants",
        "count": 45,
        "percentage": 35.4
      },
      {
        "name": "Cafes",
        "count": 28,
        "percentage": 22.0
      },
      {
        "name": "Parks",
        "count": 12,
        "percentage": 9.4
      },
      {
        "name": "Gyms",
        "count": 8,
        "percentage": 6.3
      },
      {
        "name": "Supermarkets",
        "count": 6,
        "percentage": 4.7
      },
      {
        "name": "Medical",
        "count": 10,
        "percentage": 7.9
      },
      {
        "name": "Transport",
        "count": 18,
        "percentage": 14.2
      }
    ],
    "total": 127
  }
}
```

**Response Structure:**

The response is keyed by suburb ID and contains:

**categories** (array):
| Field      | Type   | Description                       |
|------------|--------|-----------------------------------|
| name       | string | Amenity category name             |
| count      | number | Number of amenities in category   |
| percentage | number | Percentage of total amenities     |

**total** (number): Total count of all amenities

**Error Responses:**
- `404 Not Found` - Amenities not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API (NSW) / Fallback (others)

---

### 5. Get Market Trends

Get market trend data including price history and market indicators.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/market-trends
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/melbourne-3000/market-trends"
```

**Success Response (200 OK):**
```json
{
  "melbourne-3000": {
    "priceHistory": [
      {
        "month": "Jan",
        "price": 720000
      },
      {
        "month": "Feb",
        "price": 730000
      },
      {
        "month": "Mar",
        "price": 735000
      }
    ],
    "quarterlyGrowth": 5.2,
    "rentalYield": 3.4,
    "daysOnMarket": 32
  }
}
```

**Response Structure:**

The response is keyed by suburb ID and contains:

**priceHistory** (array):
| Field | Type   | Description                |
|-------|--------|----------------------------|
| month | string | Month name                 |
| price | number | Median price for the month |

**Market Indicators:**
| Field           | Type   | Description                          |
|-----------------|--------|--------------------------------------|
| quarterlyGrowth | number | Quarterly price growth percentage    |
| rentalYield     | number | Annual rental yield percentage       |
| daysOnMarket    | number | Average days properties stay on market |

**Error Responses:**
- `404 Not Found` - Market trends not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API (NSW) / Fallback (others)

---

### 6. Get Schools

Get information about nearby schools including type, sector, and ratings.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/schools
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/melbourne-3000/schools"
```

**Success Response (200 OK):**
```json
{
  "melbourne-3000": {
    "schools": [
      {
        "name": "Melbourne Central Primary School",
        "type": "Primary",
        "sector": "Government",
        "rating": 4.5,
        "distance": 0.8
      },
      {
        "name": "St. Patrick's College",
        "type": "Secondary",
        "sector": "Catholic",
        "rating": 4.3,
        "distance": 1.2
      }
    ],
    "total": 8
  }
}
```

**Response Structure:**

The response is keyed by suburb ID and contains:

**schools** (array):
| Field    | Type   | Description                              |
|----------|--------|------------------------------------------|
| name     | string | School name                              |
| type     | string | School type (Primary, Secondary, etc.)   |
| sector   | string | School sector (Government, Catholic, etc.)|
| rating   | number | School rating out of 5                   |
| distance | number | Distance from suburb center in km        |

**total** (number): Total number of schools

**Error Responses:**
- `404 Not Found` - Schools not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API (NSW) / Fallback (others)

---

### 7. Get Developments

Get information about development applications in the suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/developments
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/melbourne-3000/developments"
```

**Success Response (200 OK):**
```json
{
  "melbourne-3000": {
    "developments": [
      {
        "id": "dev-1",
        "name": "Collins Street Tower",
        "type": "Residential",
        "status": "Approved",
        "units": 245,
        "address": "123 Collins St",
        "applicant": "Urban Development Corp",
        "submittedDate": "2024-08-15"
      },
      {
        "id": "dev-2",
        "name": "Southbank Apartments",
        "type": "Mixed Use",
        "status": "Under Review",
        "units": 180,
        "address": "45 Southbank Blvd",
        "applicant": "Melbourne Property Group",
        "submittedDate": "2024-09-20"
      }
    ],
    "total": 23,
    "showing": 5
  }
}
```

**Response Structure:**

The response is keyed by suburb ID and contains:

**developments** (array):
| Field         | Type   | Description                              |
|---------------|--------|------------------------------------------|
| id            | string | Development identifier                   |
| name          | string | Development name                         |
| type          | string | Development type (Residential, Commercial, etc.) |
| status        | string | Application status (Approved, Under Review, etc.) |
| units         | number | Number of units (0 for non-residential)  |
| address       | string | Development address                      |
| applicant     | string | Applicant/developer name                 |
| submittedDate | string | Date submitted (YYYY-MM-DD format)       |

**Summary Fields:**
| Field   | Type   | Description                           |
|---------|--------|---------------------------------------|
| total   | number | Total number of developments          |
| showing | number | Number of developments in response    |

**Error Responses:**
- `404 Not Found` - Developments not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API (NSW) / Fallback (others)

---

## Extended Endpoints

### 8. Get Market Insights

Get detailed market insights with optional filters.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/market-insights
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter     | Type   | Required | Description                    |
|---------------|--------|----------|--------------------------------|
| metric        | string | No       | Specific metric filter         |
| property_type | string | No       | Property type (house, unit)    |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/market-insights?property_type=house"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                    |
|---------|--------|--------------------------------|
| results | array  | Array of market insight data   |
| total   | number | Total number of results        |

**Error Responses:**
- `404 Not Found` - Market insights not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 9. Get Pocket Insights

Get pocket-level (neighborhood) market insights.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/pocket-insights
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter     | Type    | Required | Description                       |
|---------------|---------|----------|-----------------------------------|
| geojson       | boolean | No       | Include GeoJSON data (default: true) |
| property_type | string  | No       | Property type filter              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/pocket-insights?geojson=true"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                      |
|---------|--------|----------------------------------|
| results | array  | Array of pocket insight data     |
| total   | number | Total number of pockets analyzed |

**Error Responses:**
- `404 Not Found` - Pocket insights not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 10. Get Street Insights

Get street-level market analysis and trends.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/street-insights
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter     | Type    | Required | Description                       |
|---------------|---------|----------|-----------------------------------|
| geojson       | boolean | No       | Include GeoJSON data (default: true) |
| property_type | string  | No       | Property type filter              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/street-insights"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                    |
|---------|--------|--------------------------------|
| results | array  | Array of street insight data   |
| total   | number | Total number of streets analyzed |

**Error Responses:**
- `404 Not Found` - Street insights not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

**Note:** This endpoint does not support the `geojson` parameter in the API call itself (handled internally).

---

### 11. Get Risk Factors

Get risk factor analysis for a suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/risk
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter | Type    | Required | Description                       |
|-----------|---------|----------|-----------------------------------|
| geojson   | boolean | No       | Include GeoJSON data (default: true) |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/risk"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                    |
|---------|--------|--------------------------------|
| results | array  | Array of risk factor data      |
| total   | number | Total number of risk factors   |

**Error Responses:**
- `404 Not Found` - Risk factors not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 12. Get Suburb Info

Get basic geographical information about a suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/info
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter | Type    | Required | Description                       |
|-----------|---------|----------|-----------------------------------|
| geojson   | boolean | No       | Include GeoJSON data (default: true) |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/info"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                        |
|---------|--------|------------------------------------|
| results | array  | Array of geographical info         |
| total   | number | Total number of info items         |

**Error Responses:**
- `404 Not Found` - Suburb info not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 13. Get Suburb Summary

Get AI-generated suburb summary and livability scores.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/summary
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/summary"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                      |
|---------|--------|----------------------------------|
| results | array  | Array of summary data and scores |
| total   | number | Total number of summary items    |

**Error Responses:**
- `404 Not Found` - Suburb summary not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 14. Get School Catchments

Get school catchment area information for a suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/catchments
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter | Type    | Required | Description                       |
|-----------|---------|----------|-----------------------------------|
| geojson   | boolean | No       | Include GeoJSON data (default: true) |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/catchments"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                      |
|---------|--------|----------------------------------|
| results | array  | Array of catchment area data     |
| total   | number | Total number of catchment areas  |

**Error Responses:**
- `404 Not Found` - School catchments not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 15. Get Zoning

Get zoning information for a suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/zoning
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter | Type    | Required | Description                       |
|-----------|---------|----------|-----------------------------------|
| geojson   | boolean | No       | Include GeoJSON data (default: true) |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/zoning"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                    |
|---------|--------|--------------------------------|
| results | array  | Array of zoning data           |
| total   | number | Total number of zoning areas   |

**Error Responses:**
- `404 Not Found` - Zoning info not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

### 16. Get Similar Suburbs

Get a list of suburbs similar to the specified suburb.

**Endpoint:**
```
GET /api/suburb/{suburb_id}/similar
```

**Path Parameters:**

| Parameter  | Type   | Description                    |
|------------|--------|--------------------------------|
| suburb_id  | string | Suburb identifier              |

**Query Parameters:**

| Parameter | Type    | Required | Description                       |
|-----------|---------|----------|-----------------------------------|
| geojson   | boolean | No       | Include GeoJSON data (default: true) |

**Example Request:**
```bash
curl "http://localhost:5001/api/suburb/belmont-north-2280/similar"
```

**Success Response (200 OK):**
```json
{
  "results": [],
  "total": 0
}
```

**Response Fields:**

| Field   | Type   | Description                    |
|---------|--------|--------------------------------|
| results | array  | Array of similar suburb data   |
| total   | number | Total number of similar suburbs |

**Error Responses:**
- `404 Not Found` - Similar suburbs not found
- `500 Internal Server Error` - Server error

**Data Source:** Real API only (NSW suburbs)

---

## Error Handling

### Standard Error Response

All errors return a JSON object with an error message:

```json
{
  "error": "Error description"
}
```

### HTTP Status Codes

| Status Code | Description                                    |
|-------------|------------------------------------------------|
| 200         | Success - Request completed successfully       |
| 404         | Not Found - Requested resource doesn't exist   |
| 500         | Server Error - Internal server error occurred  |

### Common Error Messages

| Error Message                  | Cause                                    |
|--------------------------------|------------------------------------------|
| "Suburb not found"             | Invalid suburb_id provided               |
| "Demographics not found"       | No demographic data available            |
| "Amenities not found"          | No amenity data available                |
| "Market trends not found"      | No market trend data available           |
| "Schools not found"            | No school data available                 |
| "Developments not found"       | No development data available            |
| "Failed to search suburbs"     | Server error during search               |
| "Failed to get suburb details" | Server error retrieving suburb details   |

---

## Data Freshness

### Real API Data (NSW Suburbs)
- **Update Frequency:** Real-time from Microburbs API
- **Availability:** Available for NSW suburbs (e.g., Belmont North, Newcastle, etc.)
- **Coverage:** All 16 endpoints with live data

### Fallback Data (Other Suburbs)
- **Update Frequency:** Static, manually updated
- **Availability:** Available for major Australian capitals (Melbourne, Sydney, Brisbane, Perth, Adelaide)
- **Coverage:** Core 7 endpoints with comprehensive sample data
- **Extended Endpoints:** Return empty results for non-NSW suburbs

---

## Rate Limiting

Currently, there are no rate limits applied to the API. However, the external Microburbs API may have its own rate limits for NSW suburb data.

---

## Examples

### Example 1: Get Complete Suburb Profile

```bash
# Get basic info
curl "http://localhost:5001/api/suburb/melbourne-3000"

# Get demographics
curl "http://localhost:5001/api/suburb/melbourne-3000/demographics"

# Get market trends
curl "http://localhost:5001/api/suburb/melbourne-3000/market-trends"

# Get nearby schools
curl "http://localhost:5001/api/suburb/melbourne-3000/schools"
```

### Example 2: Search and Explore

```bash
# Search for suburbs
curl "http://localhost:5001/api/suburbs/search?q=bel"

# Get details for found suburb
curl "http://localhost:5001/api/suburb/belmont-north-2280"

# Get amenities
curl "http://localhost:5001/api/suburb/belmont-north-2280/amenities"
```

### Example 3: Market Analysis

```bash
# Get market trends
curl "http://localhost:5001/api/suburb/sydney-2000/market-trends"

# Get developments
curl "http://localhost:5001/api/suburb/sydney-2000/developments"

# Get market insights (NSW only)
curl "http://localhost:5001/api/suburb/belmont-north-2280/market-insights"
```

---

## Testing

### Quick Health Check

Test if the API is running:

```bash
curl "http://localhost:5001/api/suburbs/search?q=mel"
```

### Test All Core Endpoints

```bash
# Test search
curl "http://localhost:5001/api/suburbs/search?q=melbourne"

# Test suburb details
curl "http://localhost:5001/api/suburb/melbourne-3000"

# Test demographics
curl "http://localhost:5001/api/suburb/melbourne-3000/demographics"

# Test amenities
curl "http://localhost:5001/api/suburb/melbourne-3000/amenities"

# Test market trends
curl "http://localhost:5001/api/suburb/melbourne-3000/market-trends"

# Test schools
curl "http://localhost:5001/api/suburb/melbourne-3000/schools"

# Test developments
curl "http://localhost:5001/api/suburb/melbourne-3000/developments"
```

---

## Support

For issues or questions:

1. Check logs for detailed error messages
2. Verify request parameters and suburb IDs
3. Confirm the backend server is running on port 5001
4. Review the fallback data files in `/backend/data/` for available suburbs

---

## Version

**API Version:** 1.0  
**Last Updated:** October 2025  
**Documentation Version:** 1.0

