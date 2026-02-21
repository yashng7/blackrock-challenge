# BlackRock Retirement Engine

Retirement auto-saving API platform that converts expenses into retirement investments using rounding rules, temporal constraints, and financial projections.

## Quick Start

### Build Container

```bash
docker build --no-cache -t blk-hacking-ind-yashwant-gawande .
```

### Run Container

```bash
docker run -p 5477:5477 blk-hacking-ind-yashwant-gawande
```

### Service

- **Port:** 5477
- **Base URL:** http://localhost:5477

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| POST | `/blackrock/challenge/v1/transactions:parse` | Parse expenses |
| POST | `/blackrock/challenge/v1/transactions:validator` | Validate transactions |
| POST | `/blackrock/challenge/v1/transactions:filter` | Apply temporal rules |
| POST | `/blackrock/challenge/v1/returns:nps` | NPS returns with tax benefit |
| POST | `/blackrock/challenge/v1/returns:index` | Index returns |
| GET | `/blackrock/challenge/v1/performance` | Performance metrics |

## API Documentation

Interactive docs available at:
- Swagger UI: http://localhost:5477/docs

## Run Tests

```bash
docker run --rm blk-hacking-ind-yashwant-gawande python -m pytest test/ -v
```

## Example Requests

### Parse Expenses

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:parse \
  -H "Content-Type: application/json" \
  -d '{"expenses":[{"date":"2024-01-15 10:30:00","amount":250}]}'
```

### Validate Transactions

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:validator \
  -H "Content-Type: application/json" \
  -d '{"wage":50000,"transactions":[{"date":"2024-01-15 10:30:00","amount":250,"ceiling":300,"remanent":50}]}'
```

### Filter with Temporal Rules

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:filter \
  -H "Content-Type: application/json" \
  -d '{"q":[],"p":[],"k":[{"start":"2024-01-01 00:00:00","end":"2024-12-31 23:59:59"}],"wage":50000,"transactions":[{"date":"2024-01-15 10:30:00","amount":250,"ceiling":300,"remanent":50}]}'
```

### NPS Returns

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/returns:nps \
  -H "Content-Type: application/json" \
  -d '{"age":29,"wage":50000,"inflation":5.5,"q":[],"p":[],"k":[{"start":"2024-01-01 00:00:00","end":"2024-12-31 23:59:59"}],"transactions":[{"date":"2024-01-15 10:30:00","amount":250}]}'
```

### Index Returns

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/returns:index \
  -H "Content-Type: application/json" \
  -d '{"age":29,"wage":50000,"inflation":5.5,"q":[],"p":[],"k":[{"start":"2024-01-01 00:00:00","end":"2024-12-31 23:59:59"}],"transactions":[{"date":"2024-01-15 10:30:00","amount":250}]}'
```

### Performance Metrics

```bash
curl http://localhost:5477/blackrock/challenge/v1/performance
```

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.12
- **Data Processing:** pandas, numpy
- **Metrics:** psutil
- **Testing:** pytest
- **Container:** Docker

## Author

Yashwant Gawande
