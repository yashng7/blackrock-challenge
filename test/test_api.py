import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "BlackRock Retirement Engine"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_parse():
    response = client.post("/blackrock/challenge/v1/transactions:parse", json={
        "expenses": [
            {"date": "2024-01-15 10:30:00", "amount": 250},
            {"date": "2024-01-16 14:00:00", "amount": 200},
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["transactions"]) == 2
    assert data["totalAmount"] == 450.0
    assert data["totalCeiling"] == 500.0
    assert data["totalRemanent"] == 50.0


def test_validator():
    response = client.post("/blackrock/challenge/v1/transactions:validator", json={
        "wage": 50000,
        "transactions": [
            {"date": "2024-01-15 10:30:00", "amount": 250, "ceiling": 300, "remanent": 50},
            {"date": "2024-01-16 14:00:00", "amount": -5, "ceiling": 100, "remanent": 105},
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["valid"]) == 1
    assert len(data["invalid"]) == 1
    assert data["invalid"][0]["message"] == "Negative amounts are not allowed"


def test_filter_with_inkperiod():
    response = client.post("/blackrock/challenge/v1/transactions:filter", json={
        "q": [{"fixed": 90, "start": "2024-01-01 00:00:00", "end": "2024-01-31 23:59:59"}],
        "p": [{"extra": 10, "start": "2024-01-01 00:00:00", "end": "2024-01-31 23:59:59"}],
        "k": [{"start": "2024-01-10 00:00:00", "end": "2024-01-20 00:00:00"}],
        "wage": 50000,
        "transactions": [
            {"date": "2024-01-01 00:00:00", "amount": 100, "ceiling": 100, "remanent": 0},
            {"date": "2024-01-15 10:30:00", "amount": 250, "ceiling": 300, "remanent": 50},
            {"date": "2024-01-31 23:59:59", "amount": 150, "ceiling": 200, "remanent": 50},
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["valid"]) == 3
    assert data["valid"][0]["inKPeriod"] == False
    assert data["valid"][1]["inKPeriod"] == True
    assert data["valid"][2]["inKPeriod"] == False
    assert data["valid"][0]["remanent"] == 100.0


def test_returns_nps_verification():
    response = client.post("/blackrock/challenge/v1/returns:nps", json={
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
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["savingsByDates"]) == 2
    assert data["savingsByDates"][0]["amount"] == 75.0
    assert data["savingsByDates"][1]["amount"] == 145.0
    assert data["savingsByDates"][0]["taxBenefit"] == 0
    assert data["savingsByDates"][1]["taxBenefit"] == 0


def test_returns_index_verification():
    response = client.post("/blackrock/challenge/v1/returns:index", json={
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
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["savingsByDates"]) == 2
    assert data["savingsByDates"][0]["amount"] == 75.0
    assert data["savingsByDates"][1]["amount"] == 145.0
    assert "totalTransactionAmount" in data
    assert "totalCeiling" in data


def test_performance():
    response = client.get("/blackrock/challenge/v1/performance")
    assert response.status_code == 200
    data = response.json()
    assert "time" in data
    assert "memory" in data
    assert "threads" in data
    assert "MB" in data["memory"]