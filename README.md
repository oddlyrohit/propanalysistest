# Real Estate Property Analysis Application

A full-stack web application for analyzing Australian real estate properties with suburb insights.

## 🏗️ Architecture

- **Client SPA**: React 19 + TypeScript app under `frontend/`, bootstrapped by Vite and styled with Tailwind CSS 4, Radix UI, and Recharts. Data access is centralized in `src/api/client.ts` and `src/api/suburbs.ts`.
- **Flask API Gateway**: `backend/app.py` wires up CORS, middleware, and the `suburbs` blueprint (`backend/api/suburbs.py`) to expose REST endpoints consumed by the frontend.
- **Service & Repository layer**: `DataAggregatorService` composes repositories from `backend/repositories` (API, file, composite) to merge live Microburbs responses with JSON fallbacks when `USE_MOCK_DATA=true`.
- **Cross-cutting middleware**: `backend/middleware` and `backend/utils` provide request tracking, validation, error handling, logging, and performance timing for every call.
- **Deployment workflow**: `npm run build` places the compiled SPA into `backend/static`, letting Flask serve both UI and API. Dockerfile + docker-compose.yml orchestrate local and container deployments with env vars from `config.py`.

## 📁 Project Structure

```
real_estate_property_analysis_ai_agent/
├── backend/
│   ├── api/
│   │   └── suburbs.py               # Suburb endpoints blueprint
│   ├── middleware/                  # Error handlers, request tracking, response formatters
│   ├── models/                      # Amenity/Demographic/Suburb dataclasses
│   ├── repositories/                # API/file/composite repository implementations
│   ├── services/
│   │   ├── data_aggregator.py       # Aggregates multiple data sources
│   │   └── microburbs_api.py        # Microburbs API client
│   ├── utils/                       # Logging and performance helpers
│   ├── static/                      # Frontend build output (after npm run build)
│   ├── API_DOCUMENTATION.md
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── api/                     # Fetch helpers and typed endpoints
│   │   ├── components/              # Map, charts, and shared UI pieces
│   │   ├── lib/                     # Utilities and formatters
│   │   ├── types/                   # TypeScript definitions
│   │   ├── assets/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── dist/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── eslint.config.js
│   ├── tsconfig.json
│   └── tsconfig.app.json
│
├── Dockerfile
├── docker-compose.yml
├── docker.env.example
├── DOCKER_README.md
├── QUICK_START.md
└── README.md
```

## ✨ Features

### Data Visualization
- **Overview Infomation** - overview information about the suburb including map and insights
-  **Demographics Analysis** - Age distribution and ethnicity breakdown
-  **Amenities Overview** - Nearby facilities and services
-  **Market DATA** - Price history and rental yields
- **Development Tracking** - Recent development applications

### User Experience
- 🔍 **Smart Search** - Search by suburb name, address, or postcode
- 📱 **Responsive Design** - Mobile-friendly interface
- 🎨 **Modern UI** - Beautiful design with Tailwind CSS
- ⚡ **Fast Loading** - Optimized performance with Vite

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 20.19+ or 22.12+** (Vite 7 requirement)
- **npm**
- **Docker** (optional, for containerized deployment)
- **Microburbs API Token** (for live data)

### Development Mode (Recommended)

**Terminal 1 - Start Flask Backend:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file (optional)
echo "MICROBURBS_API_TOKEN=your_token_here" > .env
echo "USE_MOCK_DATA=False" >> .env

python app.py
```

Backend runs on: **http://localhost:5001**

**Terminal 2 - Start Vite Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:5173**

**Access the app**: Open http://localhost:5173 in your browser

### Production Build

```bash
# 1. Build the frontend
cd frontend
npm install
npm run build  # Outputs to dist/

# 2. Start Flask (serves both API and static files)
cd ../backend
source venv/bin/activate

# Set environment variables
export MICROBURBS_API_TOKEN=your_token_here
export USE_MOCK_DATA=False

python app.py
```

**Access the app**: Open http://localhost:5001 in your browser

### Docker Deployment

**Option 1: Using docker-compose (Recommended)**

```bash
# Set your API token
export MICROBURBS_API_TOKEN=your_token_here

# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down
```

**Option 2: Using Docker directly**

```bash
# Build image
docker build -t microburbs-app .

# Run container
docker run -d -p 5001:5001 \
  --name microburbs-app \
  -e MICROBURBS_API_TOKEN=your_token_here \
  -e USE_MOCK_DATA=False \
  microburbs-app

# View logs
docker logs -f microburbs-app

# Stop container
docker stop microburbs-app && docker rm microburbs-app
```

**Access the app**: Open http://localhost:5001 in your browser

## 🔍 Try It Out

Search for these Australian suburbs:
Belmont North, New South Wales 2280


## 🛠️ Technology Stack

### Frontend
- **Vite** - Build tool and dev server
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS 4.x** - Styling
- **Recharts** - Data visualization
- **Radix UI** - Accessible components
- **Lucide React** - Icon library

### Backend
- **Flask 3.0** - Web framework
- **Flask-CORS** - Cross-origin support
- **Python 3.11** - Runtime

### DevOps
- **Docker** - Containerization
- **docker-compose** - Multi-container orchestration

## 📡 API Endpoints

Base URL (development): `http://localhost:5001`

All endpoints respond with JSON. Common suburb IDs follow the pattern `<suburb-name>-<postcode>` (e.g., `melbourne-3000`).

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/api/suburbs/search?q=<query>` | Fuzzy suburb search (try `Melbourne`, `Sydney`, `Perth`…) |
| `GET` | `/api/suburb/<suburb_id>` | Combined suburb overview card data |
| `GET` | `/api/suburb/<suburb_id>/demographics` | Age distribution, ethnicity, population metrics |
| `GET` | `/api/suburb/<suburb_id>/amenities` | Amenity categories, counts, and nearby services |
| `GET` | `/api/suburb/<suburb_id>/market-trends` | Median prices, rental yield, and historical trend data |
| `GET` | `/api/suburb/<suburb_id>/schools` | Nearby schools with levels and ratings |
| `GET` | `/api/suburb/<suburb_id>/developments` | Recent development applications |
| `GET` | `/api/suburb/<suburb_id>/market-insights` | Microburbs market insights (supports `metric`/`property_type` query params) |
| `GET` | `/api/suburb/<suburb_id>/pocket-insights` | Pocket-level geo insights (`geojson=true|false`) |
| `GET` | `/api/suburb/<suburb_id>/street-insights` | Street-level liveability and pricing data |
| `GET` | `/api/suburb/<suburb_id>/risk` | Risk factors such as flood, bushfire, crime |
| `GET` | `/api/suburb/<suburb_id>/info` | Geographic metadata and boundaries |
| `GET` | `/api/suburb/<suburb_id>/summary` | AI-generated suburb summary and scores |
| `GET` | `/api/suburb/<suburb_id>/catchments` | School catchment boundaries (`geojson` optional) |
| `GET` | `/api/suburb/<suburb_id>/zoning` | Zoning layers for the suburb |
| `GET` | `/api/suburb/<suburb_id>/similar` | List of similar suburbs |
| `GET` | `/api/suburbs/<suburb_id>/street-rankings` | Ranked list of streets for the given suburb |

> See `backend/API_DOCUMENTATION.md` for field-level response details and external Microburbs references.


## 🔧 Configuration

### Environment Variables

The application supports the following environment variables:

**Backend** (create `backend/.env`):
```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001

# Microburbs API Configuration
MICROBURBS_API_BASE_URL=https://www.microburbs.com.au/report_generator/api
MICROBURBS_API_TOKEN=your_token_here(right now is 'test')

# Application Settings
USE_MOCK_DATA=False  # Set to True to use mock data instead of API
API_TIMEOUT=10
LOG_LEVEL=INFO

# CORS Configuration (comma-separated origins)
CORS_ORIGINS=http://localhost:5173,http://localhost:5001
```

**Docker** (set via docker-compose.yml or command line):
- All backend environment variables can be set in `docker-compose.yml`
- Or pass via `-e` flag when using `docker run`

### Key Configuration Files

- `frontend/vite.config.ts` - Vite build settings, API proxy, path aliases
- `frontend/tsconfig.app.json` - TypeScript compiler options, path mappings
- `frontend/tailwind.config.js` - Tailwind CSS theme
- `frontend/postcss.config.js` - PostCSS plugins
- `backend/app.py` - Flask routes and CORS configuration
- `backend/config.py` - Backend configuration management
- `docker-compose.yml` - Docker services and environment variables
- `Dockerfile` - Multi-stage build (Node.js 18 + Python 3.11)

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Detailed quick start guide
- **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** - Technical implementation details
- **[API_DOCUMENTATION.md](API_DUCUMENTATION.md)** - external API details


## 🔒 Security Notes

This is a **demonstration application**:

- ⚠️ Not production-ready without additional security measures
- ⚠️ Uses Flask development server (not for production)
- ⚠️ No authentication or authorization
- ⚠️ Limited input validation on API endpoints
- ⚠️ API tokens should be kept secure (use .env files, never commit)

For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Adding authentication and authorization
- Implementing rate limiting
- Adding comprehensive input validation and sanitization
- Using HTTPS with proper SSL certificates
- Storing API keys securely (environment variables, secrets management)
- Adding database instead of mock JSON files
- Setting up proper logging and monitoring

## 📈 Future Enhancements

- [x] Microburbs API integration
- [x] Docker deployment support
- [x] Interactive maps 
- [ ] User authentication and saved searches
- [ ] Property comparison tool
- [ ] Email alerts for new developments
- [ ] Advanced filtering and sorting
- [ ] Export data to PDF/Excel
- [ ] Mobile applications (React Native)
- [ ] Production WSGI server setup
- [ ] Database integration (PostgreSQL/MongoDB)

## 📝 License

This project is for and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your own use.

## 📧 Support

For questions or issues:
1. Check [QUICK_START.md](QUICK_START.md) for common solutions
2. Check the browser console and Flask logs for errors

## 🎯 Getting Started

1. Clone this repository
2. Follow the [Quick Start](#-quick-start) guide above
3. Open http://localhost:5173 in your browser
4. Search for "Belmont North" 
5. Explore the data visualizations!

---

