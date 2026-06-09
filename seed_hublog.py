"""
seed_hublog.py — Popula a API HubLog (RotaVerde)
=================================================
Schemas reais (extraídos do /docs):

  POST /clientes/   {"cpf": "111.222.333-44", "nome": "...", "endereco": "...", "telefone": "..."}
  POST /produtos/   {"produto_id": "...", "nome": "...", "preco": 1, "estoque": 0}
  POST /pedidos/    {"pedido_id": "...", "prioridade": 1, "cliente_cpf": "...",
                     "produto_id": "...", "quantidade": 1, "timestamp": 0}

Uso:
    python -m pip install httpx faker
    python seed_hublog.py
"""

import os, time, random, uuid
import httpx
from faker import Faker

BASE_URL     = os.getenv("BASE_URL", "http://localhost:8000")
TIMEOUT      = 10.0
N_CLIENTES   = 8_000
N_PRODUTOS   = 1_500
N_PEDIDOS    = 3_200
BATCH_REPORT = 500

fake = Faker("pt_BR")
random.seed(42)

# ── Dados temáticos RotaVerde ─────────────────────────────────────────────────
PRODUTOS_BASE = [
    "Alface Crespa","Alface Americana","Rúcula","Espinafre","Couve",
    "Acelga","Agrião","Chicória","Tomate Cereja","Tomate Caqui",
    "Tomate Italiano","Cenoura","Beterraba","Batata Doce","Mandioca",
    "Chuchu","Abobrinha","Pepino","Berinjela","Pimentão Verde",
    "Pimentão Vermelho","Brócolis","Couve-Flor","Repolho","Quiabo",
    "Jiló","Abóbora","Cará","Inhame","Banana Nanica","Banana Prata",
    "Manga Tommy","Mamão Papaia","Abacaxi Pérola","Laranja Pera",
    "Limão Tahiti","Maracujá Amarelo","Caju","Goiaba","Acerola",
    "Açaí","Arroz Integral","Feijão Carioca","Feijão Preto","Lentilha",
    "Grão-de-Bico","Quinoa","Chia","Linhaça","Coentro","Salsinha",
    "Cebolinha","Manjericão","Alecrim","Hortelã","Gengibre","Cúrcuma",
    "Alho","Cebola","Cebola Roxa","Alho-Poró","Cogumelo Shiitake",
    "Cogumelo Paris","Cogumelo Portobello","Espiga de Milho",
]
SUFIXOS = ["Orgânico","Hidropônico","Premium","Selecionado","da Época","Fresco","","",""]

BAIRROS = [
    "Centro","Cohama","Calhau","Ponta d'Areia","Renascença","Turu",
    "São Francisco","Olho d'Água","Angelim","Anil","Vinhais",
    "Jardim Renascença","Parque Atlântico","João Paulo","Coroadinho",
    "Sacavém","Bequimão","Cidade Operária","Cohatrac","Tibiri",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def gerar_cpf_formatado() -> str:
    """Gera CPF com dígitos verificadores reais, formato 111.222.333-44."""
    n = [random.randint(0, 9) for _ in range(9)]
    s = sum((10 - i) * n[i] for i in range(9))
    d1 = 0 if (s % 11) < 2 else 11 - (s % 11)
    n.append(d1)
    s = sum((11 - i) * n[i] for i in range(10))
    d2 = 0 if (s % 11) < 2 else 11 - (s % 11)
    n.append(d2)
    d = "".join(map(str, n))
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

def nome_produto(i: int) -> str:
    base   = PRODUTOS_BASE[i % len(PRODUTOS_BASE)]
    sufixo = random.choice(SUFIXOS)
    return f"{base} {sufixo}".strip()

def pedido_id(i: int) -> str:
    return f"PED-{i:05d}"

def produto_id(i: int) -> str:
    return f"PROD-{i:05d}"

# ── Seeds ─────────────────────────────────────────────────────────────────────
def seed_clientes(client: httpx.Client) -> list[str]:
    print(f"\n{'='*60}")
    print(f"  Cadastrando {N_CLIENTES:,} clientes...")
    print(f"{'='*60}")

    cpfs_usados: set[str] = set()
    cpfs_ok: list[str] = []
    erros = 0
    primeiro_erro = None
    t0 = time.perf_counter()

    for i in range(1, N_CLIENTES + 1):
        # CPF único nesta rodada
        for _ in range(20):
            cpf = gerar_cpf_formatado()
            if cpf not in cpfs_usados:
                cpfs_usados.add(cpf)
                break

        payload = {
            "cpf":      cpf,
            "nome":     fake.name(),
            "endereco": f"Rua {fake.street_name()}, {random.randint(1,999)} — {random.choice(BAIRROS)}, São Luís-MA",
            "telefone": f"98{random.randint(10000000, 99999999)}",
        }
        try:
            r = client.post(f"{BASE_URL}/clientes/", json=payload, timeout=TIMEOUT)
            if r.status_code in (200, 201):
                cpfs_ok.append(cpf)
            else:
                erros += 1
                if primeiro_erro is None:
                    primeiro_erro = f"HTTP {r.status_code} → {r.text[:200]}"
        except Exception as e:
            erros += 1
            if primeiro_erro is None:
                primeiro_erro = str(e)

        if i % BATCH_REPORT == 0:
            elapsed = time.perf_counter() - t0
            print(f"  [{i:>6}/{N_CLIENTES}]  {i/elapsed:>6.0f} req/s  |  ok: {len(cpfs_ok):>5}  erros: {erros}")

    elapsed = time.perf_counter() - t0
    print(f"\n  ✓ Clientes: {len(cpfs_ok):,} inseridos | {erros} erros | {elapsed:.1f}s")
    if primeiro_erro:
        print(f"  ⚠ Primeiro erro: {primeiro_erro}")
    return cpfs_ok


def seed_produtos(client: httpx.Client) -> list[str]:
    print(f"\n{'='*60}")
    print(f"  Cadastrando {N_PRODUTOS:,} produtos...")
    print(f"{'='*60}")

    ids_ok: list[str] = []
    erros = 0
    primeiro_erro = None
    t0 = time.perf_counter()

    for i in range(1, N_PRODUTOS + 1):
        pid = produto_id(i)
        payload = {
            "produto_id": pid,
            "nome":       nome_produto(i),
            "preco":      round(random.uniform(1.50, 89.90), 2),
            "estoque":    random.randint(10, 500),
        }
        try:
            r = client.post(f"{BASE_URL}/produtos/", json=payload, timeout=TIMEOUT)
            if r.status_code in (200, 201):
                ids_ok.append(pid)
            else:
                erros += 1
                if primeiro_erro is None:
                    primeiro_erro = f"HTTP {r.status_code} → {r.text[:200]}"
        except Exception as e:
            erros += 1
            if primeiro_erro is None:
                primeiro_erro = str(e)

        if i % BATCH_REPORT == 0:
            elapsed = time.perf_counter() - t0
            print(f"  [{i:>5}/{N_PRODUTOS}]  {i/elapsed:>6.0f} req/s  |  ok: {len(ids_ok):>4}  erros: {erros}")

    elapsed = time.perf_counter() - t0
    print(f"\n  ✓ Produtos: {len(ids_ok):,} inseridos | {erros} erros | {elapsed:.1f}s")
    if primeiro_erro:
        print(f"  ⚠ Primeiro erro: {primeiro_erro}")
    return ids_ok


def seed_pedidos(client: httpx.Client, cpfs: list[str], pids: list[str]) -> int:
    print(f"\n{'='*60}")
    print(f"  Enfileirando {N_PEDIDOS:,} pedidos (Festival Orgânico)...")
    print(f"{'='*60}")

    # Distribuição: 10% p1, 20% p2, 40% p3, 20% p4, 10% p5
    pesos = [1,2,2,3,3,3,3,4,4,5]
    inseridos = 0
    erros = 0
    primeiro_erro = None
    t0 = time.perf_counter()
    ts_base = int(t0)

    for i in range(1, N_PEDIDOS + 1):
        payload = {
            "pedido_id":   pedido_id(i),
            "prioridade":  random.choice(pesos),
            "cliente_cpf": random.choice(cpfs),
            "produto_id":  random.choice(pids),
            "quantidade":  random.randint(1, 10),
            "timestamp":   ts_base + i,   # timestamp crescente → FIFO em prioridade igual
        }
        try:
            r = client.post(f"{BASE_URL}/pedidos/", json=payload, timeout=TIMEOUT)
            if r.status_code in (200, 201):
                inseridos += 1
            else:
                erros += 1
                if primeiro_erro is None:
                    primeiro_erro = f"HTTP {r.status_code} → {r.text[:200]}"
        except Exception as e:
            erros += 1
            if primeiro_erro is None:
                primeiro_erro = str(e)

        if i % BATCH_REPORT == 0:
            elapsed = time.perf_counter() - t0
            print(f"  [{i:>5}/{N_PEDIDOS}]  {i/elapsed:>6.0f} req/s  |  ok: {inseridos:>4}  erros: {erros}")

    elapsed = time.perf_counter() - t0
    print(f"\n  ✓ Pedidos: {inseridos:,} inseridos | {erros} erros | {elapsed:.1f}s")
    if primeiro_erro:
        print(f"  ⚠ Primeiro erro: {primeiro_erro}")
    return inseridos


def seed_distancias(client: httpx.Client):
    """Popula a matriz de distâncias com os bairros de São Luís."""
    print(f"\n{'='*60}")
    print(f"  Populando matriz de distâncias ({len(BAIRROS)} bairros)...")
    print(f"{'='*60}")

    inseridas = 0
    for i, origem in enumerate(BAIRROS):
        for j, destino in enumerate(BAIRROS):
            if i >= j:
                continue   # evita duplicatas e auto-referência
            # distância fictícia proporcional à posição na lista
            km = round(random.uniform(1.5, 35.0), 1)
            payload = {"origem": origem, "destino": destino, "distancia_km": km}
            try:
                r = client.post(f"{BASE_URL}/distancias/", json=payload, timeout=TIMEOUT)
                if r.status_code in (200, 201):
                    inseridas += 1
            except:
                pass

    print(f"  ✓ {inseridas} pares de distância inseridos")


def benchmark(client: httpx.Client):
    print(f"\n{'='*60}")
    print("  Benchmark pós-seed")
    print(f"{'='*60}")
    try:
        r = client.get(f"{BASE_URL}/benchmark", timeout=30.0)
        d = r.json()
        fila  = d.get("fila_pedidos", {})
        busca = d.get("busca_clientes", {})
        ord_  = d.get("comparacao_ordenacao", {})
        print(f"\n  Fila de Pedidos")
        print(f"    Antes  ({fila['antes']['algoritmo']}): {fila['antes']['tempo_s']}s")
        print(f"    Depois ({fila['depois']['algoritmo']}): {fila['depois']['tempo_s']}s")
        print(f"    Speedup: {fila['speedup']}")
        print(f"\n  Busca de Clientes (1.000 buscas)")
        print(f"    Antes  ({busca['antes']['algoritmo']}): {busca['antes']['tempo_1000_buscas_s']}s")
        print(f"    Depois ({busca['depois']['algoritmo']}): {busca['depois']['tempo_1000_buscas_s']}s")
        print(f"    Speedup: {busca['speedup']}")
        print(f"\n  Ordenação — projeção teórica n=3.200")
        print(f"    Bubble Sort: {ord_['bubble_sort']['operacoes_3200']:,} operações")
        print(f"    Timsort:     {ord_['timsort']['operacoes_aprox_3200']:,} operações")
    except Exception as e:
        print(f"  ✗ Erro no benchmark: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"""
╔══════════════════════════════════════════════════════════╗
║         SEED — HubLog RotaVerde  (Festival Orgânico)     ║
╠══════════════════════════════════════════════════════════╣
║  Target   : {BASE_URL:<47}║
║  Clientes : {N_CLIENTES:>6,}                                          ║
║  Produtos : {N_PRODUTOS:>6,}                                          ║
║  Pedidos  : {N_PEDIDOS:>6,}                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    try:
        with httpx.Client() as probe:
            probe.get(f"{BASE_URL}/", timeout=5.0)
        print("  ✓ API respondendo em", BASE_URL)
    except Exception:
        print(f"  ✗ Não consegui conectar em {BASE_URL}")
        print("    Suba a API primeiro:")
        print("    python -m uvicorn main:app --reload")
        return

    t_total = time.perf_counter()

    with httpx.Client() as client:
        cpfs = seed_clientes(client)
        pids = seed_produtos(client)

        if not cpfs or not pids:
            print("\n  ✗ Seed abortado — verifique os erros acima.")
            return

        seed_pedidos(client, cpfs, pids)
        seed_distancias(client)
        benchmark(client)

    elapsed = time.perf_counter() - t_total
    print(f"\n{'='*60}")
    print(f"  Seed concluído em {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()