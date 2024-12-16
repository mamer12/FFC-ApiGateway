from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.auth import API_KEY_STORAGE
from app.routes import erp  # Import the routes

app = FastAPI(title="ERPNext Integration API")

# Middleware for API key validation
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if request.url.path in ["/", "/api/v1/generate-api-key", "/api/v1/new-invoice-request", "/api/v1/loan-payment"]:
        return await call_next(request)

    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key not in API_KEY_STORAGE:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)

# Include routes
app.include_router(erp.router, prefix="/api/v1")
