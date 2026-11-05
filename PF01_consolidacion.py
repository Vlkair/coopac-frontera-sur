# 07_portafolio/PF01_consolidacion.py
import pandas as pd

CANDIDATOS = pd.DataFrame([
 # codigo, nombre, fuente, seccion_origen, objetivo, categoria
 ("C-01","Gobierno del dato maestro","Brecha de arquitectura","Sección 5.4.2 PT-01","OD-02, OD-03","Transformar"),
 ("C-02","Registro de actividades de tratamiento","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-03","Capa de integración de servicios","Brecha de arquitectura","Sección 5.4.2 PT-02","OD-01, OD-03","Transformar"),
 ("C-04","Rediseño y adopción del canal digital B2B","Brecha de servicio digital","Sección 6.1.7 S-01","OD-01","Crecer"),
 ("C-05","Consulta de estado de pedido en autoservicio","Brecha de servicio digital","Sección 6.1.7 S-02","OD-01","Crecer"),
 ("C-06","Planificación de rutas y trazabilidad de despacho","Estrategia FODA","Sección 3.5 E-02","OD-03","Crecer"),
 ("C-07","Tablero de gestión comercial","Brecha de arquitectura","Sección 5.4.2 PT-05","OD-02","Crecer"),
 ("C-08","Mesa de servicio de TI","Brecha de capacidad","Sección 4.3.5 DSS02","OD-04","Operar"),
 ("C-09","Continuidad de infraestructura y respaldo inmutable","Brecha de capacidad","Sección 4.3.5 DSS04","OD-04","Operar"),
 ("C-10","Renovación de la plataforma del ERP","Estrategia FODA","Sección 3.5 E-04","OD-04","Operar"),
 ("C-11","Programa de cumplimiento de datos personales","Obligación normativa","Sección 4.1.5","OD-05","Operar"),
 ("C-12","Gestión del conocimiento y de la configuración","Estrategia FODA","Sección 3.5 E-07","OD-06","Operar"),
 ("C-13","Comité de gobierno de TI","Brecha de capacidad","Sección 4.3.5 EDM01","OD-02, OD-04","Operar"),
 ("C-14","Instrumentación de monitoreo y disponibilidad","Brecha de línea base","Sección 6.1.5","OD-04","Operar"),
 ("C-15","Autoservicio de trabajadores (boletas y vacaciones)","Brecha de servicio digital","Sección 6.1.7 S-06, S-07","OD-01","Crecer"),
], columns=["codigo","nombre","fuente","seccion_origen","objetivo","categoria"])

FUENTES_VALIDAS = {"Obligación normativa","Brecha de arquitectura","Brecha de capacidad",
                   "Estrategia FODA","Brecha de servicio digital","Brecha de línea base"}

print("=== CONTROL DE ADMISIÓN ===")
inv = CANDIDATOS[~CANDIDATOS.fuente.isin(FUENTES_VALIDAS)]
print(f"Candidatos sin fuente admisible: {len(inv)} → se retiran: {list(inv.codigo)}")
sin_obj = CANDIDATOS[CANDIDATOS.objetivo.isna() | (CANDIDATOS.objetivo.astype(str).str.strip()=="")]
print(f"Candidatos sin objetivo asociado: {len(sin_obj)} → se retiran o se justifican")

p = CANDIDATOS[CANDIDATOS.fuente.isin(FUENTES_VALIDAS) & CANDIDATOS.objetivo.notna()].copy()
p["codigo"] = ["PR-%02d" % (i+1) for i in range(len(p))]
p.to_csv("PF01_portafolio_candidatos.csv", index=False)

print(f"\nProyectos admitidos: {len(p)}")
print("\nPor fuente:\n", p.fuente.value_counts().to_string())
print("\nPor categoría:\n", p.categoria.value_counts().to_string())
print("\n=== COBERTURA DE OBJETIVOS ===")
obj = p.objetivo.str.split(", ").explode().value_counts()
print(obj.to_string())
print("→ Todo objetivo de la sección 6.2 debe tener al menos un proyecto. Verificar los ausentes.")
