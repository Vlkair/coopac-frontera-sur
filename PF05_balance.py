# 07_portafolio/PF05_balance.py
import pandas as pd, matplotlib.pyplot as plt

p   = pd.read_csv("PF01_portafolio_candidatos.csv")
tco = pd.read_csv("PF02_tco.csv")
d   = p.merge(tco, on="codigo")

bal = d.groupby("categoria").agg(
    proyectos=("codigo","count"),
    inversion=("inv_inicial","sum"),
    tco=("tco_5","sum")).reset_index()
bal["pct_inv"] = (bal.inversion/bal.inversion.sum()*100).round(1)
bal["pct_tco"] = (bal.tco/bal.tco.sum()*100).round(1)

REF = {"Operar":(50,70), "Crecer":(20,30), "Transformar":(10,20)}
print("=== BALANCE DEL PORTAFOLIO ===")
print(bal.to_string(index=False))
print("\nContraste con las proporciones de referencia:")
for _, r in bal.iterrows():
    lo, hi = REF.get(r.categoria, (0,100))
    est = "dentro del rango" if lo <= r.pct_tco <= hi else ("POR DEBAJO" if r.pct_tco < lo else "POR ENCIMA")
    print(f"  {r.categoria:12s}: {r.pct_tco:5.1f} % del TCO  (referencia {lo}–{hi} %)  → {est}")

# Contraste con el balance ACTUAL del presupuesto (Sección 3.1)
print("\n=== COMPARACIÓN CON EL BALANCE ACTUAL DE LA ORGANIZACIÓN ===")
print("  Balance actual (Sección 3.1, presupuesto del año en curso): Operar 100 % · Crecer 8 % · Transformar 0 %")
print("  Balance propuesto por el plan          : ver arriba")
print("→ El PETI debe explicar explícitamente el cambio de balance que propone.")

fig, ax = plt.subplots(1, 2, figsize=(13,5))
COL = {"Operar":"#16285C","Crecer":"#0EA5E9","Transformar":"#F59E0B"}
ax[0].pie(bal.tco, labels=bal.categoria, autopct="%1.1f%%",
          colors=[COL[c] for c in bal.categoria], startangle=90)
ax[0].set_title("Balance del portafolio por TCO a 5 años")
ax[1].barh(d.sort_values("tco_5").codigo, d.sort_values("tco_5").tco_5,
           color=[COL[c] for c in d.sort_values("tco_5").categoria])
ax[1].set_xlabel("TCO a 5 años (S/)"); ax[1].set_title("TCO por proyecto")
plt.tight_layout(); plt.savefig("../graficos/PF_balance.png", dpi=140)
