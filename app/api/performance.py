from fastapi import APIRouter
from app.models.schemas import PerformanceResponse
from app.engines.performance import get_performance_metrics

router = APIRouter(prefix="/blackrock/challenge/v1")


@router.get("/performance", response_model=PerformanceResponse)
def performance():
    metrics = get_performance_metrics()
    return PerformanceResponse(
        time=metrics["time"],
        memory=metrics["memory"],
        threads=metrics["threads"],
    )