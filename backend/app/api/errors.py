from fastapi import Request
from fastapi.responses import JSONResponse

def register_handlers(app):
    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})


