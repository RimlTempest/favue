from fastapi import APIRouter
from app.api.routes.holo_member import router as holo_router


router = APIRouter()
router.include_router(holo_router, prefix="/holo_member", tags=["holo_member"])