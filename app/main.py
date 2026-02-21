import time
import uvicorn
from fastapi import FastAPI, Request
from app.api.root import router as root_router
from app.api.parse import router as parse_router
from app.api.validator import router as validator_router
from app.api.filter import router as filter_router
from app.api.returns import router as returns_router
from app.api.performance import router as performance_router
from app.engines.performance import set_request_time

app = FastAPI(
    title="BlackRock Retirement Engine",
    version="1.0.0",
)


@app.middleware("http")
async def track_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    if "/returns:" in request.url.path:
        set_request_time(duration)
    return response


app.include_router(root_router)
app.include_router(parse_router)
app.include_router(validator_router)
app.include_router(filter_router)
app.include_router(returns_router)
app.include_router(performance_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5477, reload=False)