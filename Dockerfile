# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci --production=false

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Python runtime
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend from stage 1 to backend static folder
COPY --from=frontend-builder /app/frontend/dist ./static

# Create necessary directories
RUN mkdir -p data services static

# Set environment variables
ENV FLASK_ENV=production \
    FLASK_DEBUG=False \
    PORT=5001 \
    PYTHONUNBUFFERED=1 \
    USE_MOCK_DATA=False

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5001/api/suburbs/search?q=test || exit 1

# Run the application
CMD ["python", "app.py"]

