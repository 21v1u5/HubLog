from fastapi import APIRouter, HTTPException
from models.schemas import ClienteIn, ProdutoIn
from core.state import clientes, produtos, historico

router_clientes = APIRouter(prefix="/clientes", tags=["Clientes"])
router_produtos = APIRouter(prefix="/produtos", tags=["Produtos"])


# ── CLIENTES ─────────────────────────────────────────────────────────────────

@router_clientes.post("/", summary="Cadastrar cliente — O(1)")
def cadastrar_cliente(body: ClienteIn):
    try:
        c = clientes.cadastrar(body.cpf, body.nome, body.endereco, body.telefone)
        historico.registrar("cadastrar_cliente", {})
        return {"ok": True, "cliente": c}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router_clientes.get("/{cpf}", summary="Buscar cliente — O(1) amortizado (era O(n))")
def buscar_cliente(cpf: str):
    c = clientes.buscar(cpf)
    if not c:
        raise HTTPException(404, "Cliente não encontrado.")
    return c


@router_clientes.delete("/{cpf}", summary="Remover cliente — O(1)")
def remover_cliente(cpf: str):
    snapshot = clientes.buscar(cpf)
    if not clientes.remover(cpf):
        raise HTTPException(404, "Cliente não encontrado.")
    historico.registrar("remover_cliente", snapshot)
    return {"ok": True}


@router_clientes.get("/", summary="Listar todos os clientes — O(n)")
def listar_clientes():
    return {"total": clientes.total(), "clientes": clientes.listar()}


# ── PRODUTOS ─────────────────────────────────────────────────────────────────

@router_produtos.post("/", summary="Adicionar produto — O(1), duplicata verificada em O(1)")
def adicionar_produto(body: ProdutoIn):
    try:
        p = produtos.adicionar(body.produto_id, body.nome, body.preco, body.estoque)
        historico.registrar("adicionar_produto", {})
        return {"ok": True, "produto": p}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router_produtos.get("/{produto_id}", summary="Buscar produto — O(1)")
def buscar_produto(produto_id: str):
    p = produtos.buscar(produto_id)
    if not p:
        raise HTTPException(404, "Produto não encontrado.")
    return p


@router_produtos.patch("/{produto_id}/estoque", summary="Atualizar estoque — O(1)")
def atualizar_estoque(produto_id: str, delta: int):
    if not produtos.atualizar_estoque(produto_id, delta):
        raise HTTPException(404, "Produto não encontrado.")
    return {"ok": True, "produto": produtos.buscar(produto_id)}


@router_produtos.delete("/{produto_id}", summary="Remover produto — O(1)")
def remover_produto(produto_id: str):
    snapshot = produtos.buscar(produto_id)
    if not produtos.remover(produto_id):
        raise HTTPException(404, "Produto não encontrado.")
    historico.registrar("remover_produto", snapshot)
    return {"ok": True}


@router_produtos.get("/", summary="Listar catálogo — O(n)")
def listar_produtos():
    return {"total": produtos.total(), "produtos": produtos.listar()}
