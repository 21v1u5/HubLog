from pydantic import BaseModel, Field
from typing import Optional


class ClienteIn(BaseModel):
    cpf: str = Field(..., example="111.222.333-44")
    nome: str
    endereco: str
    telefone: str


class ProdutoIn(BaseModel):
    produto_id: str
    nome: str
    preco: float = Field(..., gt=0)
    estoque: int = Field(..., ge=0)


class PedidoIn(BaseModel):
    pedido_id: str
    prioridade: int = Field(..., ge=1, le=5, description="1=urgente, 5=normal")
    cliente_cpf: str
    produto_id: str
    quantidade: int = Field(..., gt=0)
    timestamp: Optional[float] = None


class DistanciaIn(BaseModel):
    origem: str
    destino: str
    distancia_km: float = Field(..., gt=0)


class AcaoIn(BaseModel):
    acao: str
    dados_anteriores: dict
