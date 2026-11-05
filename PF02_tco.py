# 07_portafolio/PF02_tco.py
import pandas as pd

PROYECTOS = pd.DataFrame([
 # codigo, inversion_inicial, licencias_anual, infraestructura_anual, soporte_pct,
 # personal_anual, capacitacion_inicial, migracion, integracion, meses, incertidumbre
 ("PR-01", 55000,  6000,  3600, .15, 24000, 6000,  12000,  8000, 6, "±30 %"),
 ("PR-02", 18000,     0,     0, .10,  9000, 3000,      0,     0, 3, "±20 %"),
 ("PR-03", 78000, 12000,  9600, .18, 36000, 8000,      0, 15000, 8, "±40 %"),
 ("PR-04", 92000,  8400,  7200, .15, 30000,12000,   6000, 18000, 9, "±35 %"),
 ("PR-05", 34000,  4800,  3600, .15, 12000, 4000,   5000,  9000, 5, "±30 %"),
 ("PR-06", 28000,  3600,  2400, .15, 12000, 5000,   3000,  7000, 4, "±25 %"),
 ("PR-07", 15000,     0,  1800, .10,  6000, 3000,      0,  2000, 3, "±20 %"),
 ("PR-08", 42000,     0,  6000, .12, 12000, 4000,      0,     0, 4, "±25 %"),
 ("PR-09",145000, 24000, 12000, .18, 48000,20000,  35000, 30000,12, "±50 %"),
 ("PR-10", 22000,     0,     0, .10, 18000, 6000,      0,     0, 5, "±25 %"),
 ("PR-11",  6000,     0,     0, .00,  3000, 2000,      0,     0, 2, "±15 %"),
 ("PR-12", 19000,  2400,  1200, .12,  6000, 3000,      0,  4000, 3, "±25 %"),
 ("PR-13", 26000,  3600,  2400, .15,  9000, 5000,   4000,  6000, 4, "±30 %"),
], columns=["codigo","inv_inicial","licencias","infra","soporte_pct","personal",
            "capacitacion","migracion","integracion","meses","incertidumbre"])

AÑOS = 5
P = PROYECTOS.copy()
P["soporte_anual"] = (P.inv_inicial * P.soporte_pct).round(0)
P["costo_anual"]   = P.licencias + P.infra + P.soporte_anual + P.personal
P["costo_unico"]   = P.inv_inicial + P.capacitacion + P.migracion + P.integracion
P["tco_5"]         = P.costo_unico + P.costo_anual * AÑOS
P["pct_operativo"] = ((P.costo_anual * AÑOS) / P.tco_5 * 100).round(1)

P = P.sort_values("tco_5", ascending=False)
P.to_csv("PF02_tco.csv", index=False)

print("=== COSTO TOTAL DE PROPIEDAD A 5 AÑOS ===")
print(P[["codigo","inv_inicial","costo_unico","costo_anual","tco_5","pct_operativo","incertidumbre"]]
      .to_string(index=False))
print(f"\nInversión inicial total : S/ {P.inv_inicial.sum():,.0f}")
print(f"TCO total a 5 años      : S/ {P.tco_5.sum():,.0f}")
print(f"Factor TCO/inversión    : {P.tco_5.sum()/P.inv_inicial.sum():.2f}×")
print("\n→ El TCO es {:.1f} veces la inversión inicial. Presentar solo la inversión".format(
      P.tco_5.sum()/P.inv_inicial.sum()))
print("  inicial ante la gerencia subestima el compromiso en S/ {:,.0f}.".format(
      P.tco_5.sum()-P.inv_inicial.sum()))

print("\n=== PROYECTOS CON MAYOR PROPORCIÓN DE COSTO OPERATIVO ===")
print(P.nlargest(4,"pct_operativo")[["codigo","tco_5","pct_operativo"]].to_string(index=False))
print("→ Estos comprometen el presupuesto recurrente durante años: exigen mayor escrutinio.")
