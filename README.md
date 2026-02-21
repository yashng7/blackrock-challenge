# BlackRock Retirement Engine

A production-grade retirement auto-saving API platform that converts daily expenses into retirement investments using intelligent rounding rules, temporal constraints, and financial projections with inflation-adjusted returns.

---

## Demo Video

A 5-minute walkthrough demonstrating all endpoints, official verification, and test execution:

🎥 [Watch Demo](https://www.loom.com/share/d7fdffc584d646049c9b03be7d67fd50)

---

## Table of Contents

- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
- [Verification](#verification)
- [Tech Stack](#tech-stack)
- [Author](#author)

---

## Quick Start

### Prerequisites

- Docker installed and running

### Option 1: Docker Hub — Just Run

```bash
docker pull yashng7/blk-hacking-ind-yashwant-gawande:latest
docker run -p 5477:5477 yashng7/blk-hacking-ind-yashwant-gawande:latest
```

### Option 2: Source Code — Build and Explore

```bash
git clone https://github.com/yashng7/blackrock-challenge.git
cd blackrock-challenge
docker build --no-cache -t blk-hacking-ind-yashwant-gawande .
docker run -p 5477:5477 blk-hacking-ind-yashwant-gawande
```

### Verify

```bash
curl http://localhost:5477/health
```

Expected response:
```json
{"status": "healthy"}
```

### Service Details

| Property | Value |
|----------|-------|
| Port | 5477 |
| Base URL | http://localhost:5477 |
| API Docs | http://localhost:5477/docs |
| Docker Image | `yashng7/blk-hacking-ind-yashwant-gawande:latest` |
| Source Code | `https://github.com/yashng7/blackrock-challenge` |

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Service information |
| `GET` | `/health` | Health check |
| `POST` | `/blackrock/challenge/v1/transactions:parse` | Parse raw expenses into transactions |
| `POST` | `/blackrock/challenge/v1/transactions:validator` | Validate transaction data |
| `POST` | `/blackrock/challenge/v1/transactions:filter` | Apply temporal rules (q/p/k) |
| `POST` | `/blackrock/challenge/v1/returns:nps` | Calculate NPS returns with tax benefit |
| `POST` | `/blackrock/challenge/v1/returns:index` | Calculate Index fund returns |
| `GET` | `/blackrock/challenge/v1/performance` | System performance metrics |

Full interactive documentation available at: **http://localhost:5477/docs**

---

## Testing

### Run Tests (Docker Hub)

```bash
docker run --rm yashng7/blk-hacking-ind-yashwant-gawande:latest python -m pytest test/ -v
```

Results display directly in terminal. No source code needed.

### Run Tests (From Source)

```bash
git clone https://github.com/yashng7/blackrock-challenge.git
cd blackrock-challenge
docker build --no-cache -t blk-hacking-ind-yashwant-gawande .
docker run --rm blk-hacking-ind-yashwant-gawande python -m pytest test/ -v
```

### Generate Test Reports (From Source Only)

Test reports require source code cloned locally. The volume mount saves reports to your machine.

**Windows (PowerShell):**
```powershell
docker run --rm -v "${PWD}/test:/app/test" blk-hacking-ind-yashwant-gawande python -m pytest test/ -v
```

**Windows (Command Prompt):**
```cmd
docker run --rm -v "%cd%/test:/app/test" blk-hacking-ind-yashwant-gawande python -m pytest test/ -v
```

**Linux / macOS:**
```bash
docker run --rm -v "$(pwd)/test:/app/test" blk-hacking-ind-yashwant-gawande python -m pytest test/ -v
```

Reports generated at:

| Report | Location |
|--------|----------|
| HTML Report | `test/report.html` |
| XML Report | `test/report.xml` |

---

## Troubleshooting

### Clean Setup (Docker Hub)

**Linux / macOS:**
```bash
docker stop $(docker ps -q) 2>/dev/null
docker rmi yashng7/blk-hacking-ind-yashwant-gawande:latest 2>/dev/null
docker pull yashng7/blk-hacking-ind-yashwant-gawande:latest
docker run -p 5477:5477 yashng7/blk-hacking-ind-yashwant-gawande:latest
```

**Windows (PowerShell):**
```powershell
docker stop $(docker ps -q) 2>$null
docker rmi yashng7/blk-hacking-ind-yashwant-gawande:latest 2>$null
docker pull yashng7/blk-hacking-ind-yashwant-gawande:latest
docker run -p 5477:5477 yashng7/blk-hacking-ind-yashwant-gawande:latest
```

### Clean Rebuild (From Source)

**Linux / macOS:**
```bash
cd blackrock-challenge
docker stop $(docker ps -q) 2>/dev/null
docker rmi blk-hacking-ind-yashwant-gawande 2>/dev/null
docker build --no-cache -t blk-hacking-ind-yashwant-gawande .
docker run -p 5477:5477 blk-hacking-ind-yashwant-gawande
```

**Windows (PowerShell):**
```powershell
cd blackrock-challenge
docker stop $(docker ps -q) 2>$null
docker rmi blk-hacking-ind-yashwant-gawande 2>$null
docker build --no-cache -t blk-hacking-ind-yashwant-gawande .
docker run -p 5477:5477 blk-hacking-ind-yashwant-gawande
```

### Port Conflict Resolution

```bash
docker stop $(docker ps -q)
netstat -ano | findstr :5477
```

### Container Diagnostics

```bash
docker ps
docker logs $(docker ps -q)
curl http://localhost:5477/health
```

---

## Examples

### Parse Expenses

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:parse \
  -H "Content-Type: application/json" \
  -d '{
    "expenses": [
      {"date": "2024-01-15 10:30:00", "amount": 250},
      {"date": "2024-01-16 14:00:00", "amount": 375}
    ]
  }'
```

### Validate Transactions

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:validator \
  -H "Content-Type: application/json" \
  -d '{
    "wage": 50000,
    "transactions": [
      {"date": "2024-01-15 10:30:00", "amount": 250, "ceiling": 300, "remanent": 50}
    ]
  }'
```

### Apply Temporal Filters

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:filter \
  -H "Content-Type: application/json" \
  -d '{
    "q": [],
    "p": [],
    "k": [{"start": "2024-01-01 00:00:00", "end": "2024-12-31 23:59:59"}],
    "wage": 50000,
    "transactions": [
      {"date": "2024-01-15 10:30:00", "amount": 250, "ceiling": 300, "remanent": 50}
    ]
  }'
```

### Calculate NPS Returns

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/returns:nps \
  -H "Content-Type: application/json" \
  -d '{
    "age": 29,
    "wage": 50000,
    "inflation": 5.5,
    "q": [],
    "p": [],
    "k": [{"start": "2024-01-01 00:00:00", "end": "2024-12-31 23:59:59"}],
    "transactions": [
      {"date": "2024-01-15 10:30:00", "amount": 250}
    ]
  }'
```

### Calculate Index Returns

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/returns:index \
  -H "Content-Type: application/json" \
  -d '{
    "age": 29,
    "wage": 50000,
    "inflation": 5.5,
    "q": [],
    "p": [],
    "k": [{"start": "2024-01-01 00:00:00", "end": "2024-12-31 23:59:59"}],
    "transactions": [
      {"date": "2024-01-15 10:30:00", "amount": 250}
    ]
  }'
```

### Performance Metrics

```bash
curl http://localhost:5477/blackrock/challenge/v1/performance
```

---

## Verification

### Official Test Case

The following request matches the official verification example from the problem statement:

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/returns:nps \
  -H "Content-Type: application/json" \
  -d '{
    "age": 29,
    "wage": 50000,
    "inflation": 5.5,
    "q": [{"fixed": 0, "start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59"}],
    "p": [{"extra": 25, "start": "2023-10-01 00:00:00", "end": "2023-12-31 23:59:59"}],
    "k": [
      {"start": "2023-03-01 00:00:00", "end": "2023-11-30 23:59:59"},
      {"start": "2023-01-01 00:00:00", "end": "2023-12-31 23:59:59"}
    ],
    "transactions": [
      {"date": "2023-02-28 10:00:00", "amount": 375},
      {"date": "2023-07-01 12:00:00", "amount": 620},
      {"date": "2023-10-12 14:00:00", "amount": 250},
      {"date": "2023-12-17 16:00:00", "amount": 480}
    ]
  }'
```

### Expected Response

```json
{
  "totalTransactionAmount": 1725.0,
  "totalCeiling": 1900.0,
  "savingsByDates": [
    {
      "start": "2023-03-01 00:00:00",
      "end": "2023-11-30 23:59:59",
      "amount": 75.0,
      "profit": 44.94,
      "taxBenefit": 0.0
    },
    {
      "start": "2023-01-01 00:00:00",
      "end": "2023-12-31 23:59:59",
      "amount": 145.0,
      "profit": 86.88,
      "taxBenefit": 0.0
    }
  ]
}
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.12 |
| Data Processing | pandas, numpy |
| Performance Metrics | psutil |
| Testing | pytest |
| Container | Docker |
| Base Image | python:3.12-slim (Debian) |

---

## Project Structure

```
blackrock-retirement-engine/
├── app/
│   ├── api/           # API route handlers
│   ├── engines/       # Business logic engines
│   ├── models/        # Pydantic schemas
│   └── main.py        # Application entry point
├── test/              # Test suite
├── Dockerfile         # Container configuration
├── requirements.txt   # Python dependencies
└── README.md          # Documentation
```

---

## Author

**Yashwant Gawande**

---

## License

This project was developed as part of the BlackRock Hackathon challenge.