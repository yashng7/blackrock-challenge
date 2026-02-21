from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "service": "BlackRock Retirement Engine",
        "status": "running",
        "version": "1.0.0",
    }


@router.get("/health")
def health():
    return {
        "status": "healthy",
    }