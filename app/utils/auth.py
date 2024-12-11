from fastapi import HTTPException, Request

# Temporary storage for API keys (use a database in production)
API_KEY_STORAGE = {}

def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key not in API_KEY_STORAGE:
        raise HTTPException(status_code=401, detail="Unauthorized")
