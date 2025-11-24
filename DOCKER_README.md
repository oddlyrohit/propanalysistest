# Docker Deployment Guide

This guide explains how to build and run the Real Estate Property Analysis AI Agent using Docker.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

## Quick Start

### 1. Build the Docker Image

```bash
docker-compose build
```

### 2. Run the Application

```bash
docker-compose up -d
```

The application will be available at `http://localhost:5001`

### 3. View Logs

```bash
docker-compose logs -f
```

### 4. Stop the Application

```bash
docker-compose down
```

## Configuration

### Environment Variables

You can configure the application using environment variables in `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MICROBURBS_API_TOKEN` | `test` | Your Microburbs API token |
| `MICROBURBS_API_BASE_URL` | `https://www.microburbs.com.au/report_generator/api` | API base URL |
| `USE_MOCK_DATA` | `False` | Force use of mock data |
| `API_TIMEOUT` | `10` | API request timeout (seconds) |
| `LOG_LEVEL` | `INFO` | Logging level |
| `PORT` | `5001` | Application port |

### Custom API Token

To use a custom API token, set it before starting:

```bash
export MICROBURBS_API_TOKEN=your_token_here
docker-compose up -d
```

Or modify `docker-compose.yml`:

```yaml
environment:
  - MICROBURBS_API_TOKEN=your_token_here
```

## Docker Commands

### Build Only

```bash
docker build -t microburbs-app .
```

### Run Without Compose

```bash
docker run -d \
  -p 5001:5001 \
  -e MICROBURBS_API_TOKEN=test \
  --name microburbs-app \
  microburbs-app
```

### Execute Commands in Container

```bash
docker-compose exec app bash
```

### View Application Logs

```bash
docker-compose logs -f app
```

### Restart the Application

```bash
docker-compose restart
```

### Remove Everything

```bash
docker-compose down -v
docker rmi microburbs-app
```

## Architecture

The Docker setup uses a multi-stage build:

### Stage 1: Frontend Builder
- Uses Node.js 18 Alpine
- Installs dependencies
- Builds React frontend
- Outputs to `/dist` folder

### Stage 2: Python Runtime
- Uses Python 3.11 Slim
- Installs Flask and dependencies
- Copies backend code
- Copies built frontend to `/static`
- Runs Flask application

## Health Check

The container includes a health check that:
- Runs every 30 seconds
- Checks `/api/suburbs/search?q=test` endpoint
- Has a 10-second timeout
- Allows 3 retries
- Waits 40 seconds before first check

View health status:

```bash
docker ps
```

Look for the "STATUS" column showing "(healthy)" or "(unhealthy)".

## Troubleshooting

### Container Won't Start

1. Check logs:
   ```bash
   docker-compose logs app
   ```

2. Verify port 5001 is not in use:
   ```bash
   lsof -i :5001
   ```

### Frontend Not Loading

1. Verify frontend was built:
   ```bash
   docker-compose exec app ls -la static/
   ```

2. Check for `index.html` in static folder

### API Errors

1. Check API token is set:
   ```bash
   docker-compose exec app env | grep MICROBURBS
   ```

2. Test API directly:
   ```bash
   docker-compose exec app curl http://localhost:5001/api/suburbs/search?q=test
   ```

### Permission Issues

If you get permission errors, try:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Production Deployment

### Recommended Settings

1. Use a reverse proxy (nginx, Traefik)
2. Enable HTTPS
3. Set strong API token
4. Use environment variables for secrets
5. Enable log aggregation
6. Set up monitoring

### Example nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker Compose Production

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: microburbs-app
    ports:
      - "127.0.0.1:5001:5001"  # Only bind to localhost
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - MICROBURBS_API_TOKEN=${MICROBURBS_API_TOKEN}
      - LOG_LEVEL=WARNING
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Performance Optimization

### Multi-Stage Build Benefits

- **Smaller Image**: Only production files in final image
- **Faster Builds**: Frontend and backend built in parallel
- **Better Security**: No development tools in production

### Image Size

Expected image sizes:
- Frontend builder: ~400MB (discarded)
- Final image: ~200MB

### Build Cache

To speed up builds, Docker caches layers. To clear cache:

```bash
docker-compose build --no-cache
```

## Security Notes

1. **Never commit API tokens** to version control
2. **Use secrets management** in production (Docker Secrets, Vault)
3. **Run as non-root user** (consider adding in Dockerfile)
4. **Scan images** for vulnerabilities:
   ```bash
   docker scan microburbs-app
   ```
5. **Keep base images updated**:
   ```bash
   docker-compose build --pull
   ```

## Monitoring

### Container Stats

```bash
docker stats microburbs-app
```

### Health Status

```bash
docker inspect --format='{{.State.Health.Status}}' microburbs-app
```

### Application Metrics

Access at: `http://localhost:5001/api/suburbs/search?q=test`

## Backup and Restore

### Backup Data

If you add persistent volumes:

```bash
docker-compose exec app tar czf /tmp/backup.tar.gz data/
docker cp microburbs-app:/tmp/backup.tar.gz ./backup.tar.gz
```

### Restore Data

```bash
docker cp ./backup.tar.gz microburbs-app:/tmp/
docker-compose exec app tar xzf /tmp/backup.tar.gz -C /app/
```

## Updates

### Update Application

1. Pull latest code:
   ```bash
   git pull origin main
   ```

2. Rebuild and restart:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

### Zero-Downtime Updates

For production, use:

```bash
docker-compose build
docker-compose up -d --no-deps --build app
```

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Review health status: `docker ps`
3. Test API endpoints manually
4. Check environment variables are set correctly

## Summary

✅ **Multi-stage build** for optimized images  
✅ **Health checks** for reliability  
✅ **Environment variables** for configuration  
✅ **Production-ready** with proper settings  
✅ **Easy deployment** with docker-compose  
✅ **Full documentation** for troubleshooting

