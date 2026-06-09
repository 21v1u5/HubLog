
import heapq
import random
import time
import sys
import os

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))
from core.estruturas import (
    CadastroClientes,
    CatalogoProdutos,
    FilaPedidos,
    HistoricoAcoes,
    MatrizDistancias,
    ordenar_painel_entregador,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HubLog OS — RotaVerde",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (dark theme matching DESIGN.md) ───────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #131313; }
  [data-testid="stHeader"]           { background: transparent; }
  [data-testid="stSidebar"]          { background: #0e0e0e; }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background: rgba(26,26,26,0.55);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 18px;
  }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e5e2e1; font-weight: 300; font-size: 2.4rem; letter-spacing: -0.02em;
  }
  div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #8e90a2; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(26,26,26,0.4); border-radius: 10px; padding: 4px; }
  .stTabs [data-baseweb="tab"]      { border-radius: 8px; color: #8e90a2; font-size: 13px; padding: 6px 14px; }
  .stTabs [aria-selected="true"]    { background: rgba(184,195,255,0.12) !important; color: #b8c3ff !important; border: 1px solid rgba(184,195,255,0.25) !important; }

  /* Buttons */
  .stButton > button {
    background: rgba(184,195,255,0.1) !important;
    border: 1px solid rgba(184,195,255,0.3) !important;
    color: #b8c3ff !important; border-radius: 8px; font-size: 13px;
    transition: all 0.2s;
  }
  .stButton > button:hover {
    background: rgba(184,195,255,0.2) !important;
    border-color: rgba(184,195,255,0.5) !important;
  }
  .stButton > button[kind="primary"] {
    background: rgba(45,91,255,0.25) !important;
    border-color: rgba(45,91,255,0.6) !important;
    color: #b8c3ff !important;
  }

  /* Inputs */
  .stTextInput > div > div > input,
  .stNumberInput > div > div > input {
    background: rgba(8,8,8,0.8) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e5e2e1 !important; border-radius: 8px;
  }

  /* DataFrames */
  [data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
  [data-testid="stDataFrame"] table { background: rgba(26,26,26,0.5) !important; }

  /* Text overrides */
  h1, h2, h3, h4, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e5e2e1 !important; }
  p, li, .stMarkdown p { color: #c4c5d9; }
  code { color: #b8c3ff !important; background: rgba(184,195,255,0.08) !important; border-radius: 4px; padding: 1px 5px; }

  /* Divider */
  hr { border-color: rgba(255,255,255,0.08) !important; }

  /* Alert boxes */
  [data-testid="stAlert"] { border-radius: 10px !important; }

  /* Badge */
  .badge-green {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,121,128,0.2); border: 1px solid rgba(0,219,231,0.3);
    border-radius: 9999px; padding: 3px 14px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    color: #00dbe7; text-transform: uppercase; font-family: monospace;
  }

  /* Complexity pill */
  .pill-before { background:rgba(255,180,171,0.1); border:1px solid rgba(255,180,171,0.25);
    border-radius:6px; padding:2px 8px; color:#ffb4ab; font-family:monospace; font-weight:bold; }
  .pill-after  { background:rgba(0,219,231,0.1); border:1px solid rgba(0,219,231,0.25);
    border-radius:6px; padding:2px 8px; color:#00dbe7; font-family:monospace; font-weight:bold; }

  /* Order row */
  .order-row {
    display:flex; align-items:center; gap:10px;
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
    border-radius:8px; padding:8px 12px; margin-bottom:4px;
    font-size:13px; font-family:monospace; color:#c4c5d9;
  }
  .prio-1 { color:#ffb4ab; }
  .prio-2 { color:#ffb4ab; opacity:.75; }
  .prio-3 { color:#b8c3ff; }
  .prio-4 { color:#8e90a2; }
  .prio-5 { color:#434656; }
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
_DEFAULTS = {
    "clientes":      CadastroClientes,
    "produtos":      CatalogoProdutos,
    "fila":          FilaPedidos,
    "historico":     HistoricoAcoes,
    "distancias":    MatrizDistancias,
    "pedidos_snap":  list,
    "bench_result":  lambda: None,
}
for key, factory in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = factory()

# ── Header ───────────────────────────────────────────────────────────────────
col_hdr, col_badge = st.columns([4, 1])
with col_hdr:
    st.markdown("# 🚚 HUBLOG OS — RotaVerde")
    st.markdown("**Reestruturação de Estruturas de Dados** · UNDB 2026.1 · Prof. Esp. Guilherme Ferreira dos Reis")
with col_badge:
    st.markdown(
        '<div style="text-align:right;padding-top:22px">'
        '<span class="badge-green">● SISTEMA OPERANTE</span>'
        "</div>",
        unsafe_allow_html=True,
    )

st.divider()

# ── Metric cards ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("👥 Clientes",        st.session_state.clientes.total(),  help="Hash Map (dict) · Busca O(1)")
with m2:
    st.metric("📦 Produtos",        st.session_state.produtos.total(),  help="Set + Dict · Duplicata O(1)")
with m3:
    st.metric("🚚 Pedidos na Fila", st.session_state.fila.tamanho(),   help="Min-Heap (heapq) · Extração O(log n)")
with m4:
    st.metric("↩ Histórico",       st.session_state.historico.tamanho(), help="Pilha LIFO (deque) · O(1)")

st.markdown("")

# ── Tabs ─────────────────────────────────────────────────────────────────────
t_bench, t_complex, t_clientes, t_produtos, t_pedidos, t_hist = st.tabs([
    "⚡ Benchmark",
    "🔬 Complexidade",
    "👥 Clientes",
    "📦 Produtos",
    "🚚 Pedidos",
    "↩ Histórico",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB: BENCHMARK
# ════════════════════════════════════════════════════════════════════════════
with t_bench:
    st.subheader("Benchmark de Performance")
    st.markdown(
        "> **Cenário:** Festival Orgânico da Primavera · "
        "3.200 pedidos realizados em menos de 40 minutos — situação real do colapso do HubLog"
    )

    if st.button("▶ Executar Benchmark agora", type="primary"):
        N = 3200

        with st.spinner("Executando simulação..."):
            # ── FILA ANTES: varredura linear O(n) por extração → O(n²) total
            lista_antiga = [{"id": i, "prioridade": random.randint(1, 5)} for i in range(N)]
            t0 = time.perf_counter()
            for _ in range(N):
                if lista_antiga:
                    m = min(lista_antiga, key=lambda x: x["prioridade"])
                    lista_antiga.remove(m)
            t_fila_antes = time.perf_counter() - t0

            # ── FILA DEPOIS: min-heap O(log n) por operação
            heap = []
            for i in range(N):
                heapq.heappush(heap, (random.randint(1, 5), i))
            t0 = time.perf_counter()
            for _ in range(N):
                if heap:
                    heapq.heappop(heap)
            t_fila_depois = time.perf_counter() - t0

            speedup_fila = round(t_fila_antes / t_fila_depois, 1) if t_fila_depois > 0 else 0

            # ── BUSCA ANTES: lista sequencial O(n)
            lista_cl = [{"cpf": str(i)} for i in range(8000)]
            cpf_alvo = str(random.randint(0, 7999))
            t0 = time.perf_counter()
            for _ in range(1000):
                next((c for c in lista_cl if c["cpf"] == cpf_alvo), None)
            t_busca_antes = time.perf_counter() - t0

            # ── BUSCA DEPOIS: hash map O(1)
            dict_cl = {str(i): {"cpf": str(i)} for i in range(8000)}
            t0 = time.perf_counter()
            for _ in range(1000):
                dict_cl.get(cpf_alvo)
            t_busca_depois = time.perf_counter() - t0

            speedup_busca = round(t_busca_antes / t_busca_depois, 1) if t_busca_depois > 0 else 0

        st.session_state.bench_result = {
            "speedup_fila": speedup_fila,
            "speedup_busca": speedup_busca,
            "t_fila_antes": round(t_fila_antes, 4),
            "t_fila_depois": round(t_fila_depois, 4),
            "t_busca_antes": round(t_busca_antes, 4),
            "t_busca_depois": round(t_busca_depois, 4),
        }

    r = st.session_state.bench_result
    if r:
        st.markdown("---")
        st.markdown("### Resultados em tempo real")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Fila de Pedidos — Extração do Mais Urgente**")
            st.metric("Speedup medido", f"{r['speedup_fila']}×", help="Min-Heap vs varredura linear")
            st.markdown(f"🔴 Antes (varredura linear O(n²)): `{r['t_fila_antes']}s`")
            st.markdown(f"🟢 Depois (min-heap O(n log n)): `{r['t_fila_depois']}s`")
            st.caption("Antes (100% do tempo):")
            st.progress(1.0)
            after_pct = max(0.01, 1.0 / r["speedup_fila"])
            st.caption(f"Depois ({round(after_pct*100,1)}% do tempo):")
            st.progress(after_pct)

        with c2:
            st.markdown("**Busca de Clientes — 1.000 consultas / 8.000 registros**")
            st.metric("Speedup medido", f"{r['speedup_busca']}×", help="Hash Map vs lista sequencial")
            st.markdown(f"🔴 Antes (lista sequencial O(n)): `{r['t_busca_antes']}s`")
            st.markdown(f"🟢 Depois (hash map O(1)): `{r['t_busca_depois']}s`")
            st.caption("Antes (100% do tempo):")
            st.progress(1.0)
            after_pct_b = max(0.01, 1.0 / r["speedup_busca"])
            st.caption(f"Depois ({round(after_pct_b*100,1)}% do tempo):")
            st.progress(after_pct_b)

        st.markdown("---")
        st.markdown("### Comparação de Algoritmos de Ordenação — n = 3.200 pedidos")
        ca, cb, cc = st.columns(3)
        with ca:
            st.error(
                "**Bubble Sort** *(descartado)*\n\n"
                "Complexidade: `O(n²)`\n\n"
                f"~{3200**2:,} operações no pior caso\n\n"
                "Instável · recalculado a cada atualização"
            )
        with cb:
            st.warning(
                "**Merge Sort** *(considerado)*\n\n"
                "Complexidade: `O(n log n)`\n\n"
                "~37.200 operações\n\n"
                "Estável · memória auxiliar O(n)"
            )
        with cc:
            st.success(
                "**Timsort ★ Escolhido**\n\n"
                "Complexidade: `O(n log n)` · melhor caso `O(n)`\n\n"
                "~37.200 operações\n\n"
                "Estável · adaptativo · built-in Python"
            )

        st.info(
            "**Decisão técnica:** Min-Heap (`heapq`) para extração contínua do pedido mais urgente (Módulo 3) "
            "e Timsort (`sorted` built-in) para ordenação visual do painel do entregador (Módulo 6)."
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB: COMPLEXIDADE
# ════════════════════════════════════════════════════════════════════════════
with t_complex:
    st.subheader("Análise de Complexidade — Antes vs Depois")
    st.markdown("Comparação técnica dos 6 módulos reestruturados do HubLog · RotaVerde.")

    df_complex = pd.DataFrame({
        "Módulo":             ["Cadastro de Clientes", "Catálogo de Produtos", "Fila de Pedidos",
                               "Histórico (Undo)", "Matriz de Distâncias", "Painel Entregador"],
        "Estrutura Anterior": ["Lista Sequencial", "Lista sem controle", "Varredura Linear",
                               "Estrutura incorreta", "Lista sem índice", "Bubble Sort"],
        "Estrutura Proposta": ["Hash Map (dict)", "Set + Dict", "Min-Heap (heapq)",
                               "Pilha LIFO (deque)", "Dict Aninhado", "Timsort (sorted)"],
        "Operação Crítica":   ["Busca por CPF", "Verificar duplicata", "Extrair mais urgente",
                               "Desfazer ação", "Consulta origem→destino", "Ordenar pedidos"],
        "Antes":              ["O(n)", "O(n)", "O(n)", "O(?) — bug", "O(n)", "O(n²)"],
        "Depois":             ["O(1)", "O(1)", "O(log n)", "O(1)", "O(1)", "O(n log n)"],
        "Ganho (n=3.2k)":     ["~8.000×", "~n×", "~275×", "Corrigido", "~n×", "~275×"],
    })
    st.dataframe(df_complex, use_container_width=True, hide_index=True)

    st.markdown("### Notação Assintótica — Referência Rápida")
    st.markdown("""
| Notação | Nome | Exemplo |
|---------|------|---------|
| `O(1)` | **Constante** — não cresce com n | Hash Map lookup |
| `O(log n)` | **Logarítmico** — cresce muito lentamente | Min-Heap extraction |
| `O(n)` | **Linear** — proporcional ao tamanho | Busca em lista |
| `O(n log n)` | **Quase-linear** — ótimo para ordenação | Timsort, Heap Sort |
| `O(n²)` | **Quadrático** — inaceitável para n > 1.000 | Bubble Sort |
    """)

    st.markdown("### Impacto para n = 3.200 pedidos (Festival)")
    df_ops = pd.DataFrame({
        "Algoritmo":    ["Bubble Sort", "Timsort / Heap Sort", "Min-Heap (3.200 extrações)"],
        "Complexidade": ["O(n²)", "O(n log n)", "O(n log n)"],
        "Operações":    [f"{3200**2:,}", f"~{int(3200*11.6):,}", f"~{int(3200*11.6):,}"],
        "Situação":     ["❌ Colapso", "✅ Aceitável", "✅ Aceitável"],
    })
    st.dataframe(df_ops, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB: CLIENTES
# ════════════════════════════════════════════════════════════════════════════
with t_clientes:
    st.subheader("Módulo 1: Cadastro de Clientes")
    st.markdown("""
**Estrutura:** `dict` Python (Hash Map)
**Antes:** Lista sequencial — busca percorria todos os elementos → **O(n)**
**Depois:** Dicionário indexado por CPF → busca em **O(1) amortizado**
    """)

    col_form, col_list = st.columns([2, 3])

    with col_form:
        st.markdown("**Cadastrar Cliente**")
        cpf  = st.text_input("CPF *",     placeholder="000.000.000-00", key="cl_cpf")
        nome = st.text_input("Nome *",    placeholder="Nome completo",  key="cl_nome")
        end  = st.text_input("Endereço", placeholder="Rua, bairro",    key="cl_end")
        tel  = st.text_input("Telefone", placeholder="(98) 9 0000-0000", key="cl_tel")

        if st.button("Cadastrar — Hash Map O(1)", use_container_width=True):
            if not cpf or not nome:
                st.error("CPF e Nome são obrigatórios.")
            else:
                try:
                    st.session_state.clientes.cadastrar(
                        cpf, nome,
                        end or "São Luís, MA",
                        tel or "(98) 9 0000-0000",
                    )
                    st.session_state.historico.registrar("cadastrar_cliente", {})
                    st.success(f'✓ "{nome}" inserido no Hash Map — O(1)')
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        st.markdown("---")
        st.markdown("**Buscar por CPF — O(1)**")
        cpf_busca = st.text_input("CPF", placeholder="000.000.000-00", key="cl_busca")
        if st.button("Buscar"):
            r = st.session_state.clientes.buscar(cpf_busca)
            if r:
                st.success(f"✓ **{r['nome']}** · {r['endereco']} · {r['telefone']}")
            else:
                st.error("Cliente não encontrado.")

    with col_list:
        total = st.session_state.clientes.total()
        st.markdown(f"**{total} clientes no Hash Map**")
        lista = st.session_state.clientes.listar()
        if lista:
            st.dataframe(pd.DataFrame(lista), use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum cliente cadastrado ainda. Use o formulário ao lado.")


# ════════════════════════════════════════════════════════════════════════════
# TAB: PRODUTOS
# ════════════════════════════════════════════════════════════════════════════
with t_produtos:
    st.subheader("Módulo 2: Catálogo de Produtos")
    st.markdown("""
**Estrutura:** `set` (IDs únicos) + `dict` (dados completos)
**Antes:** Lista sem controle — duplicatas passavam silenciosamente → inconsistências de estoque
**Depois:** Set verifica duplicata em **O(1)** antes de qualquer inserção
    """)

    col_form, col_list = st.columns([2, 3])

    with col_form:
        st.markdown("**Adicionar Produto**")
        prod_id   = st.text_input("ID *",    placeholder="P-001",         key="pr_id")
        prod_nome = st.text_input("Nome *",  placeholder="Nome do produto", key="pr_nome")
        col_p, col_e = st.columns(2)
        with col_p:
            preco = st.number_input("Preço (R$)", min_value=0.0, step=0.01, key="pr_preco")
        with col_e:
            estoque = st.number_input("Estoque", min_value=0, step=1, key="pr_est")

        if st.button("Adicionar — Set+Dict O(1)", use_container_width=True):
            if not prod_id or not prod_nome:
                st.error("ID e Nome são obrigatórios.")
            else:
                try:
                    st.session_state.produtos.adicionar(prod_id, prod_nome, preco, int(estoque))
                    st.session_state.historico.registrar("adicionar_produto", {})
                    st.success(f'✓ "{prod_nome}" ({prod_id}) adicionado — Set garantiu unicidade O(1)')
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    with col_list:
        total = st.session_state.produtos.total()
        st.markdown(f"**{total} produtos no catálogo** · {total} IDs únicos no Set")
        lista = st.session_state.produtos.listar()
        if lista:
            st.dataframe(pd.DataFrame(lista), use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum produto cadastrado ainda.")


# ════════════════════════════════════════════════════════════════════════════
# TAB: PEDIDOS
# ════════════════════════════════════════════════════════════════════════════
with t_pedidos:
    st.subheader("Módulo 3: Fila de Pedidos — Min-Heap")
    st.markdown("""
**Estrutura:** Min-Heap via `heapq` Python
**Antes:** Varredura completa a cada priorização → O(n) por extração → **O(n²)** no Festival
**Depois:** Extração do mais urgente em **O(log n)** · ~275× mais rápido para n=3.200
    """)

    col_ins, col_painel = st.columns([2, 3])

    with col_ins:
        st.markdown("**Inserir Pedido no Heap**")
        ped_id   = st.text_input("ID do Pedido *", placeholder="PED-001", key="ped_id")
        col_c, col_p = st.columns(2)
        with col_c:
            ped_cpf  = st.text_input("CPF",        placeholder="000...", key="ped_cpf")
        with col_p:
            ped_prod = st.text_input("Produto ID", placeholder="P-001",  key="ped_prod")

        col_pri, col_qtd = st.columns(2)
        with col_pri:
            prio = st.selectbox(
                "Prioridade",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {1:"1 — Urgente",2:"2 — Alta",3:"3 — Normal",4:"4 — Baixa",5:"5 — Mínima"}[x],
                index=2, key="ped_prio",
            )
        with col_qtd:
            qtd = st.number_input("Qtd.", min_value=1, value=1, key="ped_qtd")

        if st.button("Inserir no Min-Heap — O(log n)", use_container_width=True):
            if not ped_id:
                st.error("ID do pedido é obrigatório.")
            else:
                dados = {
                    "cliente_cpf": ped_cpf or "—",
                    "produto_id":  ped_prod or "—",
                    "quantidade":  int(qtd),
                    "timestamp":   time.time(),
                }
                st.session_state.fila.inserir(ped_id, prio, dados)
                snap = {"pedido_id": ped_id, "prioridade": prio, **dados}
                st.session_state.pedidos_snap.append(snap)
                prio_label = {1:"Urgente",2:"Alta",3:"Normal",4:"Baixa",5:"Mínima"}[prio]
                st.success(f'✓ "{ped_id}" inserido no Heap · Prioridade {prio} ({prio_label}) — O(log n)')
                st.rerun()

        st.markdown("")
        c_esp, c_ext = st.columns(2)
        with c_esp:
            if st.button("👁 Espiar Topo", use_container_width=True):
                p = st.session_state.fila.espiar_mais_urgente()
                if p:
                    st.info(f"**{p['pedido_id']}** · Prio {p['prioridade']}")
                else:
                    st.warning("Fila vazia.")
        with c_ext:
            if st.button("⏭ Extrair Próximo", use_container_width=True):
                p = st.session_state.fila.extrair_mais_urgente()
                if p:
                    st.success(f"✓ Extraído: **{p['pedido_id']}** · Prio {p['prioridade']}")
                    st.session_state.pedidos_snap = [
                        s for s in st.session_state.pedidos_snap
                        if s.get("pedido_id") != p["pedido_id"]
                    ]
                    st.rerun()
                else:
                    st.warning("Fila vazia.")

    with col_painel:
        st.markdown(
            f"**Painel do Entregador — {st.session_state.fila.tamanho()} pedidos na fila**  \n"
            "Timsort O(n log n) · ex-Bubble Sort O(n²)"
        )

        prio_icons = {1: "🔴", 2: "🟠", 3: "🔵", 4: "⚪", 5: "⬜"}
        prio_names = {1: "Urgente", 2: "Alta", 3: "Normal", 4: "Baixa", 5: "Mínima"}

        snap = st.session_state.pedidos_snap
        if snap:
            ordenados = ordenar_painel_entregador(snap)
            rows = []
            for i, p in enumerate(ordenados, 1):
                ts = time.strftime("%H:%M:%S", time.localtime(p.get("timestamp", 0)))
                rows.append({
                    "#": i,
                    "ID": p.get("pedido_id", "?"),
                    "Prioridade": f'{prio_icons.get(p["prioridade"],"?")} {prio_names.get(p["prioridade"],"?")}',
                    "CPF": p.get("cliente_cpf", "—"),
                    "Produto": p.get("produto_id", "—"),
                    "Qtd": p.get("quantidade", 1),
                    "Hora": ts,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum pedido inserido ainda. Use o formulário ao lado.")


# ════════════════════════════════════════════════════════════════════════════
# TAB: HISTÓRICO
# ════════════════════════════════════════════════════════════════════════════
with t_hist:
    st.subheader("Módulo 4: Histórico de Ações — Pilha LIFO")
    st.markdown("""
**Estrutura:** `collections.deque` usada como Pilha LIFO
**Antes:** Estrutura incorreta — retornava a ação errada ao desfazer (bug crítico no Festival)
**Depois:** LIFO garantido — sempre desfaz a **última** ação realizada · push/pop **O(1)**
    """)

    col_undo, col_stack = st.columns([1, 2])

    with col_undo:
        prof = st.session_state.historico.tamanho()
        st.metric("Profundidade da pilha", prof)

        topo = st.session_state.historico.espiar()
        if topo:
            ts = time.strftime("%H:%M:%S", time.localtime(topo["ts"]))
            st.info(f"**Topo (última ação):**\n\n`{topo['acao']}` — {ts}")
        else:
            st.info("Pilha vazia.")

        if st.button("↩ Desfazer Última Ação — LIFO O(1)", use_container_width=True):
            acao = st.session_state.historico.desfazer()
            if acao:
                st.success(f'✓ Desfeito: **{acao["acao"]}** — LIFO correto')
                st.rerun()
            else:
                st.error("Pilha vazia.")

    with col_stack:
        st.markdown("**Pilha completa (mais recente → mais antiga):**")
        pilha = list(st.session_state.historico._pilha)
        pilha.reverse()
        if pilha:
            rows = []
            for i, a in enumerate(pilha):
                ts = time.strftime("%H:%M:%S", time.localtime(a["ts"]))
                rows.append({
                    "Pos.": i + 1,
                    "Ação": a["acao"],
                    "Hora": ts,
                    "": "← TOPO" if i == 0 else "",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info(
                "Nenhuma ação registrada ainda.  \n"
                "Cadastre clientes ou produtos para ver o histórico."
            )

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;color:#434656;font-size:12px;font-family:monospace;padding-bottom:8px'>"
    "HubLog OS · RotaVerde Logística · UNDB 2026.1 · "
    "HashMap · Set · Min-Heap · Stack LIFO · Dict · Timsort"
    "</div>",
    unsafe_allow_html=True,
)
