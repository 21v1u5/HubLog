"""
Estado global do HubLog — instâncias únicas das estruturas de dados.
Em produção real, isso seria persistido em Redis/banco de dados.
"""
from core.estruturas import (
    CadastroClientes,
    CatalogoProdutos,
    FilaPedidos,
    HistoricoAcoes,
    MatrizDistancias,
)

clientes = CadastroClientes()
produtos = CatalogoProdutos()
fila_pedidos = FilaPedidos()
historico = HistoricoAcoes()
distancias = MatrizDistancias()
