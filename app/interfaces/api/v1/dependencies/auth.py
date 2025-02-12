from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import settings
security = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return credentials.credentials
