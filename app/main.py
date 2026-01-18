from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.security import verify_api_key
from app.api.routes.organizations import router as org_router
from app.api.routes.buildings import router as b_router
from app.api.routes.activities import router as a_router

app = FastAPI(title=settings.app_name, dependencies=[Depends(verify_api_key)])

app.include_router(org_router, prefix="/organizations", tags=["organizations"])
app.include_router(b_router, prefix="/buildings", tags=["buildings"])
app.include_router(a_router, prefix="/activities", tags=["activities"])
