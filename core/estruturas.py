"""
HubLog - Core de Estruturas de Dados Reestruturadas
=====================================================
Cada módulo substitui a implementação original por uma estrutura
tecnicamente adequada ao contexto, com análise de complexidade documentada.
"""

import heapq
import time
from collections import deque
from typing import Any, Optional

# MÓDULO 1 — CADASTRO DE CLIENTES
class CadastroClientes:
    """
    Hash Map para armazenamento e consulta de clientes.

    Complexidade:
        Antes  (lista sequencial): busca O(n), inserção O(1)
        Depois (dict/hash map)   : busca O(1) amort., inserção O(1) amort.
    """

    def __init__(self):
        self._dados: dict[str, dict] = {}

    # O(1) amortizado
    def cadastrar(self, cpf: str, nome: str, endereco: str, telefone: str) -> dict:
        if cpf in self._dados:
            raise ValueError(f"Cliente {cpf} já cadastrado.")
        cliente = {"cpf": cpf, "nome": nome, "endereco": endereco, "telefone": telefone}
        self._dados[cpf] = cliente
        return cliente

    # O(1) amortizado
    def buscar(self, cpf: str) -> Optional[dict]:
        return self._dados.get(cpf)

    # O(1)
    def remover(self, cpf: str) -> bool:
        return self._dados.pop(cpf, None) is not None

    # O(1)
    def total(self) -> int:
        return len(self._dados)

    def listar(self) -> list[dict]:
        return list(self._dados.values())



# MÓDULO 2 — CATÁLOGO DE PRODUTOS
class CatalogoProdutos:
    """
    Set de IDs garante unicidade; Dict armazena os dados completos.

    Complexidade:
        Antes  (lista sem controle): inserção O(1), verificação duplicata O(n)
        Depois (set + dict)        : inserção O(1), verificação duplicata O(1)
    """

    def __init__(self):
        self._ids: set[str] = set()
        self._produtos: dict[str, dict] = {}

    # O(1) — duplicata verificada pelo Set em tempo constante
    def adicionar(self, produto_id: str, nome: str, preco: float, estoque: int) -> dict:
        if produto_id in self._ids:
            raise ValueError(f"Produto '{produto_id}' já existe no catálogo.")
        produto = {
            "id": produto_id,
            "nome": nome,
            "preco": preco,
            "estoque": estoque,
        }
        self._ids.add(produto_id)
        self._produtos[produto_id] = produto
        return produto

    # O(1)
    def buscar(self, produto_id: str) -> Optional[dict]:
        return self._produtos.get(produto_id)

    # O(1)
    def atualizar_estoque(self, produto_id: str, delta: int) -> bool:
        if produto_id not in self._produtos:
            return False
        self._produtos[produto_id]["estoque"] += delta
        return True

    # O(1)
    def remover(self, produto_id: str) -> bool:
        if produto_id not in self._ids:
            return False
        self._ids.discard(produto_id)
        self._produtos.pop(produto_id, None)
        return True

    def listar(self) -> list[dict]:
        return list(self._produtos.values())

    def total(self) -> int:
        return len(self._ids)


# MÓDULO 3 — FILA DE PEDIDOS DOS ENTREGADORES
class FilaPedidos:
    """
    Min-Heap baseado em (prioridade, timestamp, pedido).
    Menor valor de prioridade = mais urgente (prioridade 1 > prioridade 5).
    Timestamps desempatam pedidos com mesma prioridade (FIFO).

    Complexidade:
        Antes  (varredura linear): inserção O(1), extração-mín O(n)
        Depois (min-heap)        : inserção O(log n), extração-mín O(log n)

    Para n=3200 pedidos:
        Antes : 3200 operações por extração
        Depois: ~12  operações por extração  (log₂ 3200 ≈ 11,6)
    """

    def __init__(self):
        self._heap: list = []
        self._counter = 0          # desempate FIFO por timestamp lógico

    # O(log n)
    def inserir(self, pedido_id: str, prioridade: int, dados: dict) -> None:
        entry = (prioridade, self._counter, pedido_id, dados)
        self._counter += 1
        heapq.heappush(self._heap, entry)

    # O(log n)
    def extrair_mais_urgente(self) -> Optional[dict]:
        if not self._heap:
            return None
        prioridade, _, pedido_id, dados = heapq.heappop(self._heap)
        return {"pedido_id": pedido_id, "prioridade": prioridade, **dados}

    # O(1)
    def espiar_mais_urgente(self) -> Optional[dict]:
        if not self._heap:
            return None
        prioridade, _, pedido_id, dados = self._heap[0]
        return {"pedido_id": pedido_id, "prioridade": prioridade, **dados}

    # O(1)
    def tamanho(self) -> int:
        return len(self._heap)

    def esta_vazia(self) -> bool:
        return len(self._heap) == 0


# MÓDULO 4 — HISTÓRICO DE AÇÕES (DESFAZER / UNDO)
class HistoricoAcoes:
    """
    Pilha LIFO para histórico de ações do usuário.
    deque é preferível à list porque append/pop na direita são O(1) garantido.

    Complexidade:
        Antes  (estrutura incorreta): O(?) — comportamento indefinido
        Depois (pilha LIFO)         : push O(1), pop O(1), peek O(1)
    """

    def __init__(self, limite: int = 50):
        self._pilha: deque = deque(maxlen=limite)

    # O(1)
    def registrar(self, acao: str, dados_anteriores: Any) -> None:
        self._pilha.append({"acao": acao, "snapshot": dados_anteriores, "ts": time.time()})

    # O(1) — LIFO correto, retorna SEMPRE a última ação realizada
    def desfazer(self) -> Optional[dict]:
        if not self._pilha:
            return None
        return self._pilha.pop()

    # O(1)
    def espiar(self) -> Optional[dict]:
        if not self._pilha:
            return None
        return self._pilha[-1]

    # O(1)
    def tamanho(self) -> int:
        return len(self._pilha)



# MÓDULO 5 — MATRIZ DE DISTÂNCIAS
class MatrizDistancias:
    """
    Dicionário aninhado indexado por (origem, destino).
    Permite lookup O(1) em vez de varredura linear.

    Complexidade:
        Antes  (lista sem índice): lookup O(n)
        Depois (dict aninhado)   : lookup O(1)
    """

    def __init__(self):
        self._matriz: dict[str, dict[str, float]] = {}

    # O(1)
    def definir(self, origem: str, destino: str, distancia_km: float) -> None:
        self._matriz.setdefault(origem, {})[destino] = distancia_km
        self._matriz.setdefault(destino, {})[origem] = distancia_km   # bidirecional

    # O(1) — era O(n) sem indexação
    def consultar(self, origem: str, destino: str) -> Optional[float]:
        return self._matriz.get(origem, {}).get(destino)

    def pontos(self) -> list[str]:
        return list(self._matriz.keys())



# MÓDULO 6 — ORDENAÇÃO DE PEDIDOS POR PRIORIDADE
def ordenar_painel_entregador(pedidos: list[dict]) -> list[dict]:
    """
    Ordena pedidos para exibição no painel.
    Usa Timsort (Python built-in sorted) → O(n log n), estável.
    Critério: prioridade ASC, depois timestamp ASC (FIFO no mesmo nível).
    """
    return sorted(pedidos, key=lambda p: (p["prioridade"], p.get("timestamp", 0)))
