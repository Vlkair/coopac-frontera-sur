# 07_portafolio/PF04_alternativas.py
import pandas as pd
AÑOS = 5

ALT = pd.DataFrame([
 # proyecto, alternativa, inv_inicial, costo_anual, beneficio_anual, descripcion
 ("PR-09","A. No hacer nada",            0,      0, -180000,
  "La plataforma pierde soporte en la fecha anunciada por el fabricante: sin parches de seguridad, riesgo de interrupción "
  "y de incumplimiento normativo. Costo estimado de una interrupción prolongada."),
 ("PR-09","B. Migrar a la versión soportada del mismo proveedor", 145000, 84000,  60000,
  "Menor riesgo de migración de datos; mantiene la dependencia del proveedor actual."),
 ("PR-09","C. Reemplazar por otra solución",                      240000, 96000, 120000,
  "Mayor costo y riesgo de migración; elimina la dependencia y habilita integración nativa."),

 ("PR-04","A. No hacer nada",            0,      0,  -95000,
  "Se mantienen 74 400 pedidos anuales por teléfono: costo de la fuerza de ventas en "
  "toma de pedidos y errores de transcripción."),
 ("PR-04","B. Rediseño móvil del portal existente",  92000, 57600, 145000,
  "Aprovecha el desarrollo existente; requiere la capa de integración (PR-03)."),
 ("PR-04","C. Nueva plataforma de comercio B2B",    210000, 84000, 175000,
  "Mayor capacidad y menor deuda técnica; mayor costo y tiempo de implantación."),
], columns=["proyecto","alternativa","inv_inicial","costo_anual","beneficio_anual","descripcion"])

ALT["costo_5"]    = ALT.inv_inicial + ALT.costo_anual * AÑOS
ALT["beneficio_5"]= ALT.beneficio_anual * AÑOS
ALT["neto_5"]     = ALT.beneficio_5 - ALT.costo_5
ALT["retorno"]    = (ALT.neto_5 / ALT.costo_5.replace(0, pd.NA) * 100).round(1)

for p, g in ALT.groupby("proyecto"):
    print(f"\n{'='*95}\n{p}")
    print(g[["alternativa","inv_inicial","costo_5","beneficio_5","neto_5","retorno"]].to_string(index=False))
    mejor = g.loc[g.neto_5.idxmax()]
    print(f"→ Mayor beneficio neto a 5 años: {mejor.alternativa} (S/ {mejor.neto_5:,.0f})")
    base = g[g.alternativa.str.startswith("A.")].iloc[0]
    print(f"→ Costo de la inacción a 5 años: S/ {abs(base.beneficio_5):,.0f}")
ALT.to_csv("PF04_alternativas.csv", index=False)
