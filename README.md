# FastAPI Web Scraper

Simple webscraper built with fastapi, postgres and redis.

## Prerequisites

- Docker Engine (27.3.1+)
- Docker Compose (2.29.7+)
- Python 3.12+

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/snifhex/fastapi-web-scraper.git
   cd fastapi-web-scraper
   ```

2. Run locally via Docker
   ```bash
   docker compose -f docker-compose.local.yaml up --build
   ```

3. Access the Swagger UI:
   - Swagger UI: http://localhost:80/docs

## Run locally via docker 

  ```bash
  docker compose -f docker-compose.local.yaml up -d
  ```

## Quick Test

```bash
# Start scraping with default settings
curl -X POST "http://localhost:80/api/v1/scrape/" \
  -H "X-API-Key: super" \
  -H "Content-Type: application/json" \
  -d '{"page_limit": 5}'

# Start scraping with proxy
curl -X POST "http://localhost:80/api/v1/scrape/" \
  -H "X-API-Key: super" \
  -H "Content-Type: application/json" \
  -d '{
    "page_limit": 5,
    "proxy": "http://your-proxy:8080"
  }'

```

## Project Structure

```bash
app/
├── api/                # API route definitions
├── common/             # Shared components
│   ├── cache/          # Caching strategies
│   ├── notification/   # Notification services
│   └── storage/        # Storage implementations
├── core/               # Db, Config, setting etc 
├── scrape/             # Scraping service
├── utils/              # Rate limiter, Retry decorator etc
└── main.py             # Application entry point
```

## Simple Diagram
```mermaid
graph TD
    A[FastAPI App] --> B[Authentication]
    B --> C[Scraper App]
    C --> D[Scraper Service]
    D --> E[Web Scraper]
    D --> I[(PostgreSQL)]
    D --> F[Storage Strategy]
    D --> G[Cache Strategy]
    D --> H[Notification Strategy]
    F --> J[S3 Storage]
    G --> K[(Redis Cache)]
    H --> L[Console Logger]
```

## Development

1. Install Dependencies
    ```
    uv sync
    ```
2. Run Linting
    ```
    ./scripts/lint.sh
    ```
3. Format code
    ```
    ./scripts/lint.sh
    ```

## Environment Variable

| Variable | Description | Default | 
|----------|-------------|---------|
| API_TOKEN | Authentication token | super |
| DATABASE_URL | Database connection | postgresql://postgres:password@localhost:5432/scraped |
| REDIS_HOST | Redis server address | localhost |
| REDIS_PORT | Redis server port | 6379 |
| AWS_ACCESS_KEY_ID | MinIO access key | minioadmin |
| AWS_SECRET_ACCESS_KEY | MinIO secret key | minioadmin |
| AWS_BUCKET_NAME | Storage bucket name | scraper-bucket |
| AWS_ENDPOINT_URL | MinIO endpoint | http://localhost:9000 |
| MAX_RETRIES | Request Max retry count | 3 | 
| MAX_DELAY | Wait time between retries | 5 | 
