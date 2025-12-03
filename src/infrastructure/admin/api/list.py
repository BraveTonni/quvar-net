from fastapi import APIRouter, Request, Depends

from src.infrastructure.admin.dto.client import ClientDTO
from src.infrastructure.admin.deps import get_bootstrap

router = APIRouter()


@router.get("/")
async def get_clients_list(request: Request, bootstrap=Depends(get_bootstrap)):
    clients = bootstrap.get_clients()
    formatted_clients = [
        ClientDTO.from_domain(client).model_dump() for client in clients
    ]

    return {"success": True, "count": len(clients), "clients": formatted_clients}
