
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "chave-secreta"

@AuthJWT.load_config
def get_config():
    return Settings()

def register_auth_exception_handler(app):
    @app.exception_handler(AuthJWTException)
    def auth_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
