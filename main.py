"""
HubLog API — RotaVerde
======================
FastAPI backend com estruturas de dados reestruturadas.

Para rodar:
    pip install fastapi uvicorn
    uvicorn main:app --reload
"""

import time
import random
import heapq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers.clientes_produtos import router_clientes, router_produtos
from routers.operacoes import (
    router_pedidos, router_historico, router_distancias, router_painel
)

app = FastAPI(
    title="HubLog API — RotaVerde",
    description="""
## Consultoria de Reestruturação de Estruturas de Dados

### Módulos reestruturados e ganho de performance

| Módulo | Estrutura anterior | Estrutura proposta | Busca/Extração |
|---|---|---|---|
| Cadastro de clientes | Lista sequencial | **Hash Map (dict)** | O(n) → **O(1)** |
| Catálogo de produtos | Lista sem controle | **Set + Dict** | O(n) → **O(1)** |
| Fila de pedidos | Varredura linear | **Min-Heap** | O(n) → **O(log n)** |
| Histórico (undo) | Estrutura incorreta | **Pilha LIFO (deque)** | — → **O(1) correto** |
| Matriz de distâncias | Lista sem índice | **Dict aninhado** | O(n) → **O(1)** |
| Ordenação do painel | Bubble Sort O(n²) | **Timsort O(n log n)** | n²→ **n log n** |
    """,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_clientes)
app.include_router(router_produtos)
app.include_router(router_pedidos)
app.include_router(router_historico)
app.include_router(router_distancias)
app.include_router(router_painel)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ── BENCHMARK EMBUTIDO ────────────────────────────────────────────────────────

@app.get("/benchmark", tags=["Benchmark"],
         summary="Demonstra ganho de performance com n=3200 pedidos (cenário Festival)")
def benchmark():
    """
    Simula o cenário do 'Festival Orgânico da Primavera' (3200 pedidos)
    comparando a implementação antiga vs nova.
    """
    N = 3200

    # ── ANTES: varredura linear O(n) para encontrar mínimo ──
    lista_antiga = [{"id": i, "prioridade": random.randint(1, 5)} for i in range(N)]
    t0 = time.perf_counter()
    for _ in range(N):
        if lista_antiga:
            minimo = min(lista_antiga, key=lambda x: x["prioridade"])
            lista_antiga.remove(minimo)
    t_antes = time.perf_counter() - t0

    # ── DEPOIS: min-heap O(log n) ──
    heap = []
    for i in range(N):
        heapq.heappush(heap, (random.randint(1, 5), i))
    t0 = time.perf_counter()
    for _ in range(N):
        if heap:
            heapq.heappop(heap)
    t_depois = time.perf_counter() - t0

    speedup = round(t_antes / t_depois, 1) if t_depois > 0 else 0

    # ── ANTES: busca linear em lista de clientes ──
    lista_clientes = [{"cpf": str(i), "nome": f"Cliente {i}"} for i in range(8000)]
    cpf_alvo = str(random.randint(0, 7999))
    t0 = time.perf_counter()
    for _ in range(1000):
        next((c for c in lista_clientes if c["cpf"] == cpf_alvo), None)
    t_busca_antes = time.perf_counter() - t0

    # ── DEPOIS: hash map O(1) ──
    dict_clientes = {str(i): {"cpf": str(i), "nome": f"Cliente {i}"} for i in range(8000)}
    t0 = time.perf_counter()
    for _ in range(1000):
        dict_clientes.get(cpf_alvo)
    t_busca_depois = time.perf_counter() - t0

    speedup_busca = round(t_busca_antes / t_busca_depois, 1) if t_busca_depois > 0 else 0

    return {
        "cenario": "Festival Orgânico da Primavera — 3200 pedidos",
        "fila_pedidos": {
            "antes":  {"algoritmo": "varredura linear (min)", "complexidade": "O(n²)", "tempo_s": round(t_antes, 4)},
            "depois": {"algoritmo": "min-heap (heapq)",       "complexidade": "O(n log n)", "tempo_s": round(t_depois, 4)},
            "speedup": f"{speedup}x mais rápido",
        },
        "busca_clientes": {
            "antes":  {"algoritmo": "lista sequencial", "complexidade": "O(n)", "tempo_1000_buscas_s": round(t_busca_antes, 4)},
            "depois": {"algoritmo": "hash map (dict)",  "complexidade": "O(1)", "tempo_1000_buscas_s": round(t_busca_depois, 4)},
            "speedup": f"{speedup_busca}x mais rápido",
        },
        "comparacao_ordenacao": {
            "bubble_sort": {"complexidade": "O(n²)", "operacoes_3200": 3200 ** 2},
            "timsort":     {"complexidade": "O(n log n)", "operacoes_aprox_3200": int(3200 * 11.6)},
            "heap_sort":   {"complexidade": "O(n log n)", "operacoes_aprox_3200": int(3200 * 11.6)},
            "escolha": "Heap para fila contínua; Timsort para painel (estável e adaptativo)",
        },
    }


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")
