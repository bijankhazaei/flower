from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_nodes():
    return {"message": "Node endpoints - TODO"}