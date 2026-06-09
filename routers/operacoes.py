import time
from fastapi import APIRouter, HTTPException
from models.schemas import PedidoIn, DistanciaIn, AcaoIn
from core.state import fila_pedidos, historico, distancias
from core.estruturas import ordenar_painel_entregador

router_pedidos = APIRouter(prefix="/pedidos", tags=["Pedidos"])
router_historico = APIRouter(prefix="/historico", tags=["Histórico"])
router_distancias = APIRouter(prefix="/distancias", tags=["Distâncias"])
router_painel = APIRouter(prefix="/painel", tags=["Painel Entregador"])

# cache simples para o painel (snapshot dos pedidos ainda na fila)
_snapshot_pedidos: list[dict] = []


# ── PEDIDOS (MIN-HEAP) ────────────────────────────────────────────────────────

@router_pedidos.post("/", summary="Inserir pedido na fila — O(log n)")
def inserir_pedido(body: PedidoIn):
    dados = {
        "cliente_cpf": body.cliente_cpf,
        "produto_id": body.produto_id,
        "quantidade": body.quantidade,
        "timestamp": body.timestamp or time.time(),
    }
    fila_pedidos.inserir(body.pedido_id, body.prioridade, dados)
    _snapshot_pedidos.append({"pedido_id": body.pedido_id,
                              "prioridade": body.prioridade,
                              "timestamp": dados["timestamp"],
                              **dados})
    return {"ok": True, "tamanho_fila": fila_pedidos.tamanho()}


@router_pedidos.get("/proximo",
                    summary="Extrair pedido mais urgente — O(log n)  [era O(n)]")
def extrair_pedido():
    pedido = fila_pedidos.extrair_mais_urgente()
    if not pedido:
        raise HTTPException(404, "Fila de pedidos vazia.")
    return pedido


@router_pedidos.get("/espiar",
                    summary="Ver pedido mais urgente sem remover — O(1)")
def espiar_pedido():
    pedido = fila_pedidos.espiar_mais_urgente()
    if not pedido:
        raise HTTPException(404, "Fila de pedidos vazia.")
    return pedido


@router_pedidos.get("/tamanho", summary="Tamanho da fila — O(1)")
def tamanho_fila():
    return {"tamanho": fila_pedidos.tamanho()}


# ── HISTÓRICO / UNDO (PILHA LIFO) ────────────────────────────────────────────

@router_historico.post("/registrar", summary="Registrar ação — O(1)")
def registrar_acao(body: AcaoIn):
    historico.registrar(body.acao, body.dados_anteriores)
    return {"ok": True, "profundidade": historico.tamanho()}


@router_historico.post("/desfazer",
                       summary="Desfazer última ação — O(1) LIFO correto [era incorreto]")
def desfazer():
    acao = historico.desfazer()
    if not acao:
        raise HTTPException(404, "Nenhuma ação para desfazer.")
    return {"desfeita": acao}


@router_historico.get("/espiar",
                      summary="Ver última ação sem desfazer — O(1)")
def espiar_historico():
    acao = historico.espiar()
    if not acao:
        raise HTTPException(404, "Histórico vazio.")
    return acao


@router_historico.get("/profundidade", summary="Quantidade de ações registradas — O(1)")
def profundidade():
    return {"profundidade": historico.tamanho()}


# ── DISTÂNCIAS (DICT ANINHADO) ───────────────────────────────────────────────

@router_distancias.post("/", summary="Definir distância — O(1)")
def definir_distancia(body: DistanciaIn):
    distancias.definir(body.origem, body.destino, body.distancia_km)
    return {"ok": True}


@router_distancias.get("/{origem}/{destino}",
                        summary="Consultar distância — O(1)  [era O(n)]")
def consultar_distancia(origem: str, destino: str):
    d = distancias.consultar(origem, destino)
    if d is None:
        raise HTTPException(404, "Rota não encontrada.")
    return {"origem": origem, "destino": destino, "distancia_km": d}


@router_distancias.get("/pontos/listar", summary="Listar pontos de entrega — O(n)")
def listar_pontos():
    return {"pontos": distancias.pontos()}


# ── PAINEL ENTREGADOR (TIMSORT) ───────────────────────────────────────────────

@router_painel.get("/",
                   summary="Painel ordenado por prioridade — O(n log n)  [era O(n²) Bubble Sort]")
def painel_entregador():
    ordenado = ordenar_painel_entregador(_snapshot_pedidos)
    return {
        "total": len(ordenado),
        "algoritmo": "Timsort — O(n log n)",
        "pedidos": ordenado,
    }
