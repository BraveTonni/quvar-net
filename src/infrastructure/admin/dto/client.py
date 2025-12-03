# src/infrastructure/admin/dto/client.py
from pydantic import BaseModel, Field
from uuid import UUID
from src.domain.entities.client import ClientInfo, ClientRole
from typing import Dict


class ClientInfoDTO(BaseModel):
    role: ClientRole
    os_info: Dict[str, str]
    local_ip: str
    user: str
    cpu: str
    ram_gb: float
    gpu: str | None = None
    is_admin: bool = False
    created_at: int

    @classmethod
    def from_domain(cls, info: ClientInfo) -> "ClientInfoDTO":
        return cls(**info.__dict__)


class ClientDTO(BaseModel):
    uuid: UUID = Field(..., description="Уникальный идентификатор клиента")
    info: ClientInfoDTO

    @classmethod
    def from_domain(cls, client) -> "ClientDTO":
        return cls(uuid=client.uuid, info=ClientInfoDTO.from_domain(client.info))
