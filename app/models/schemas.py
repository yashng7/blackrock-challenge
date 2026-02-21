from pydantic import BaseModel, ConfigDict, Field
from typing import List


class Expense(BaseModel):
    date: str
    amount: float


class TransactionOut(BaseModel):
    date: str
    amount: float
    ceiling: float
    remanent: float


class ParseRequest(BaseModel):
    expenses: List[Expense]


class ParseResponse(BaseModel):
    transactions: List[TransactionOut]
    totalAmount: float
    totalCeiling: float
    totalRemanent: float


class TransactionIn(BaseModel):
    date: str
    amount: float
    ceiling: float
    remanent: float


class InvalidTransaction(BaseModel):
    date: str
    amount: float
    ceiling: float
    remanent: float
    message: str


class ValidatorRequest(BaseModel):
    wage: float
    transactions: List[TransactionIn]


class ValidatorResponse(BaseModel):
    valid: List[TransactionOut]
    invalid: List[InvalidTransaction]


class QPeriod(BaseModel):
    fixed: float
    start: str
    end: str


class PPeriod(BaseModel):
    extra: float
    start: str
    end: str


class KPeriod(BaseModel):
    start: str
    end: str


class FilterTransactionOut(BaseModel):
    date: str
    amount: float
    ceiling: float
    remanent: float
    inKPeriod: bool


class FilterRequest(BaseModel):
    q: List[QPeriod]
    p: List[PPeriod]
    k: List[KPeriod]
    wage: float
    transactions: List[TransactionIn]


class FilterResponse(BaseModel):
    valid: List[FilterTransactionOut]
    invalid: List[InvalidTransaction]


class RawTransaction(BaseModel):
    date: str
    amount: float


class ReturnsRequest(BaseModel):
    age: float
    wage: float
    inflation: float
    q: List[QPeriod]
    p: List[PPeriod]
    k: List[KPeriod]
    transactions: List[RawTransaction]


class NPSSavings(BaseModel):
    start: str
    end: str
    amount: float
    profit: float
    taxBenefit: float


class NPSResponse(BaseModel):
    totalTransactionAmount: float
    totalCeiling: float
    savingsByDates: List[NPSSavings]


class IndexSavings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    start: str
    end: str
    amount: float
    return_: float = Field(alias="return")


class IndexResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    totalTransactionAmount: float
    totalCeiling: float
    savingsByDates: List[IndexSavings]


class PerformanceResponse(BaseModel):
    time: str
    memory: str
    threads: int