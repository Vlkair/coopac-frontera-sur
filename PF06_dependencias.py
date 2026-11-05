# 07_portafolio/PF06_dependencias.py
import pandas as pd, networkx as nx, matplotlib.pyplot as plt

DEP = [  # (proyecto, depende_de)
 ("PR-04","PR-03"), ("PR-04","PR-01"),
 ("PR-05","PR-03"),
 ("PR-06","PR-01"),
 ("PR-07","PR-01"), ("PR-07","PR-03"),
 ("PR-09","PR-03"),
 ("PR-14","PR-08"),
]
G = nx.DiGraph()
G.add_nodes_from(pd.read_csv("PF01_portafolio_candidatos.csv").codigo)
G.add_edges_from([(b,a) for a,b in DEP])     # arista de habilitador → dependiente

print("=== ORDEN TOPOLÓGICO (secuencia obligada) ===")
try:
    orden = list(nx.topological_sort(G))
    print(" → ".join(orden))
except nx.NetworkXUnfeasible:
    print("⚠ Existe un ciclo de dependencias: revisar el modelo")

print("\n=== PROYECTOS HABILITADORES (mayor grado de salida) ===")
for n, g in sorted(G.out_degree(), key=lambda x: -x[1])[:5]:
    if g: print(f"  {n}: habilita {g} proyecto(s) → prioridad estructural")

print("\n=== PROYECTOS SIN DEPENDENCIAS (pueden iniciar de inmediato) ===")
print("  " + ", ".join(n for n in G.nodes if G.in_degree(n) == 0))

pos = nx.spring_layout(G, seed=42, k=1.2)
plt.figure(figsize=(11,8))
nx.draw(G, pos, with_labels=True, node_color="#16285C", font_color="white",
        node_size=1800, font_size=9, arrows=True, arrowsize=18, edge_color="#94A3B8")
plt.title("Mapa de dependencias del portafolio")
plt.tight_layout(); plt.savefig("../graficos/PF_dependencias.png", dpi=140)
