from fastapi import APIRouter, Request, Depends

from src.infrastructure.admin.dto.client import ClientDTO
from src.infrastructure.admin.deps import get_bootstrap

router = APIRouter()


@router.get("/{uuid}")
async def info(request: Request, uuid: str, bootstrap=Depends(get_bootstrap)):
    client = bootstrap.get_client_by_uuid(uuid)

    if not client:
        return {"success": False, "error": "Client not found."}

    formatted_client = ClientDTO.from_domain(client).model_dump()

    return {"success": True, "client": formatted_client}
