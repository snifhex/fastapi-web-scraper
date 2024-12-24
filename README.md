# Fastapi 

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

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| API_TOKEN | Authentication token | super | Yes |
| DATABASE_URL | Database connection | postgresql://postgres:password@localhost:5432/scraped | Yes |
| REDIS_HOST | Redis server address | localhost | Yes |
| REDIS_PORT | Redis server port | 6379 | Yes |
| AWS_ACCESS_KEY_ID | MinIO access key | minioadmin | Yes |
| AWS_SECRET_ACCESS_KEY | MinIO secret key | minioadmin | Yes |
| AWS_BUCKET_NAME | Storage bucket name | scraper-bucket | Yes |
| AWS_ENDPOINT_URL | MinIO endpoint | http://localhost:9000 | Yes |
