"""Regenera la entrega técnica sin modificar los archivos originales."""
from contextlib import redirect_stdout
from modelo import *

OUT = ROOT/'evidencias/S13/salidas'
OUT.mkdir(parents=True,exist_ok=True)
def ejecutar(fn,name):
    with (OUT/f'{name}.txt').open('w',encoding='utf-8') as f, redirect_stdout(f):
        return fn()

ejecutar(consolidar,'PF01_consolidacion')
t = ejecutar(tco,'PF02_tco')
a = ejecutar(alternativas,'PF04_alternativas')
b = ejecutar(balance,'PF05_balance')
order,wave=ejecutar(dependencias,'PF06_dependencias')
idx={r['codigo']:r for r in t}
fichas={}
for code,x in P.items():
    z=idx[code]
    exclusions={
      'PR-01':'Reemplazo del core ni digitalización retrospectiva de todos los archivos',
      'PR-02':'Reemplazo del core ni obra de centro de datos',
      'PR-08':'Migración del core ni nuevos productos financieros',
      'PR-12':'Decisiones automáticas sobre créditos o socios',
    }.get(code,'Despliegue fuera del alcance piloto ni sustitución del core')
    campos=[
     ('Código',code),('Nombre',x['proyecto']),('Categoría',x['categoria']),
     ('Fuente y sección PETI',f"{x['fuente']} · {x['seccion_origen']} (reconstrucción de trabajo)"),
     ('Evidencia del problema',x['evidencia']),('Objetivo vinculado',x['objetivo']+' · '+OBJ[x['objetivo']]),
     ('Patrocinio propuesto','Gerencia General; aprobación pendiente'),('Responsable propuesto',x['responsable']),
     ('Alcance y entregables',x['entregable']),('Exclusiones',exclusions),
     ('Beneficiarios','Socios y personal en alcance piloto' if code in ('PR-01','PR-08','PR-10') else 'Áreas responsables de la operación y el control'),
     ('Plazo y ola',f"{x['meses']} meses estimados · ola {wave[code]+1}; no implica fecha aprobada"),
     ('Dependencias',', '.join(x['predecesores']) or 'Sin dependencia técnica interna en este escenario'),
     ('Recursos','Equipo TI de cinco personas compartido, responsable funcional y soporte externo sujeto a presupuesto'),
     ('Inversión inicial',money(x['inicial'])),('Operación anual y salida',f"{money(x['anual'])} por año; salida: {money(x['salida'])} al año 5"),
     ('TCO a cinco años',f"{money(z['tco_5'])} · factor {z['factor']:.2f}×"),
     ('Origen e incertidumbre',f"{z['referencia']}. Supuesto académico ±{x['margen_pct']} %: {money(z['tco_min'])} a {money(z['tco_max'])}."),
     ('Riesgo y respuesta','Capacidad limitada o costo mayor al previsto; aprobar por hitos, verificar alcance piloto y recotizar antes de contratar.'),
     ('Criterio de aceptación y medición',x['criterio']+'. Dueño funcional registra línea base y evidencia del piloto.'),
    ]
    assert len(campos)==20
    fichas[code]=campos
    md(HERE/'PF03_fichas'/f'{code}.md','# '+code+' · '+x['proyecto']+'\n\n'+
       '\n'.join(f'{i}. **{k}:** {v}' for i,(k,v) in enumerate(campos,1)))

IMPACTS={
 'PR-01':[
  ('Sociedad','Socios','100 % de lecturas del piloto con trazabilidad; prueba con datos anonimizados.','Privacidad y acceso autorizado; revisión de cumplimiento.'),
  ('Economía','Créditos y Finanzas','Medir horas de investigación por evento antes y después del piloto.','Sin requisito monetario inferido.'),
  ('Salud y seguridad','Analistas','No se identifica efecto directo en salud física; medir reportes de exposición de datos.','Seguridad de la información, validar matriz.'),
  ('Marco legal','Cumplimiento','100 % de roles piloto aprobados y evidencia de accesos retenida según política validada.','Protección de datos y alcance sectorial por validar.'),
  ('Medio ambiente','Operaciones','Contar hojas por expediente en piloto; no estimar ahorro sin línea base.','Disposición de soportes según política aplicable.')],
 'PR-02':[
  ('Sociedad','Socios y agencias','Medir duración de interrupciones en dos ejercicios al año.','Continuidad del servicio, validar alcance.'),
  ('Economía','TI y Finanzas','Medir horas de indisponibilidad y de recuperación.','Sin requisito monetario inferido.'),
  ('Salud y seguridad','TI','No hay efecto sanitario directo; comprobar acceso controlado a respaldos.','Seguridad de la información.'),
  ('Marco legal','Riesgos y Auditoría','Dos actas de recuperación por año; verificar meta RTO/RPO.','Obligaciones de continuidad sujetas a la matriz.'),
  ('Medio ambiente','TI','Inventariar equipos retirados y registrar entrega de medios a gestión autorizada.','Validar política de residuos y borrado.')],
 'PR-08':[
  ('Sociedad','Socios de agencias y valles','≥ 60 % de trámites elegibles completos en línea; mantener canal asistido.','Accesibilidad y privacidad; validar requisitos.'),
  ('Economía','Socios y Atención','Medir minutos de atención por solicitud y volumen; contrastar con hipótesis de 8 minutos.','Sin requisito monetario inferido.'),
  ('Salud y seguridad','Socios','No se identifica efecto sanitario directo; medir incidentes de autenticación.','Protección de credenciales y datos.'),
  ('Marco legal','Cumplimiento','100 % de flujos piloto con aviso de privacidad y revisión de permisos.','Tratamiento de datos y requisitos del canal por validar.'),
  ('Medio ambiente','Socios','Medir visitas presenciales evitadas; no convertir a emisiones sin datos de distancia y transporte.','No se identifica obligación ambiental directa para el piloto.')],
}
OPTIONS={
 'PR-01':('Permisos y bitácora sobre carpetas actuales','Repositorio controlado, migración piloto, roles y alertas','Primero evaluar módulo de gestión documental compatible; comparar adaptación libre y desarrollo propio por integración, soporte y salida.'),
 'PR-02':('Copia aislada y restauración manual','Copias aisladas, restauración automatizada y simulacros','Comparar ampliar la solución existente, adaptar herramientas abiertas y construir automatización; exigir prueba de recuperación y portabilidad.'),
 'PR-08':('Formulario y seguimiento semimanual','Trámite integrado, autenticado y con notificación al socio','Evaluar extensión del proveedor actual, adaptación libre o desarrollo propio; exigir acceso a interfaces, prueba de integración y costo de salida.')}
cases={}
for code,opts in OPTIONS.items():
    x=P[code]; rr=[r for r in a if r['codigo']==code]
    best=min(rr,key=lambda r:r['costo_economico_5'])
    assert best['alternativa']=='Solución completa'
    cutoff=(rr[2]['tco_5']-rr[1]['tco_5'])/((rr[2]['beneficio_incremental_5']-rr[1]['beneficio_incremental_5'])/CASES[code][0])
    intro=[
      ('Problema y alcance',x['evidencia']+'. '+x['entregable']+'.'),
      ('Objetivo y éxito',x['objetivo']+' · '+x['criterio']+'.'),
      ('Inacción',rr[0]['supuesto']+f". Cinco años: {money(rr[0]['inaccion_5'])} de pérdida modelada; no es gasto observado."),
      ('Opciones','Mínima: '+opts[0]+'. Completa: '+opts[1]+'. '+opts[2]),
      ('Recomendación',f"Completa en el escenario base: costo económico de {money(best['costo_economico_5'])}. Supera a la mínima si la exposición anual excede {money(cutoff)} con iguales eficacias. Revaluar con costos y medición real antes de aprobar."),
      ('Riesgo, recursos y dependencias',f"{x['responsable']}; {x['meses']} meses estimados; requiere "+', '.join(x['predecesores'])+'. Mitigar desviación con piloto, aceptación formal y revisión de beneficios a 90 y 180 días.'),
    ]
    cases[code]=dict(titulo=x['proyecto'],resumen=intro,alternativas=rr,impactos=IMPACTS[code])
    lines=[f'# Caso de negocio {code} · {x["proyecto"]}']
    lines+=['\n**'+k+'.** '+v for k,v in intro]
    lines+=['\n| Alternativa | TCO 5 años | Pérdida residual | Costo económico | Mejora neta vs inacción |','|---|---:|---:|---:|---:|']
    for r in rr:lines.append('| '+r['alternativa']+' | '+' | '.join(money(r[k]) for k in ('tco_5','beneficio_frente_escenario_ideal_5','costo_economico_5','mejora_neta_vs_inaccion'))+' |')
    lines+=['\nLa pérdida residual se presenta con signo negativo. Costo económico = TCO + pérdida residual en valor absoluto. Montos no descontados y supuestos sujetos a validación.',
            '\n| Dimensión | A quién afecta | Efecto o indicador | Aplicabilidad |','|---|---|---|---|']
    lines+=['| '+' | '.join(r)+' |' for r in IMPACTS[code]]
    md(HERE/'PF04_casos'/f'{code}.md','\n'.join(lines))

coverage={k:[c for c,x in P.items() if x['objetivo']==k] for k in OBJ}
assert all(coverage.values())
assert set(P)==set(idx) and len(P)==12
assert set(CASES)=={r['codigo'] for r in t[:3]}
assert all(z['tco_5']==z['inversion_inicial']+5*z['costo_anual']+z['salida_ano_5'] and z['costo_anual']>0 for z in t)
assert all(order.index(d)<order.index(c) for c,x in P.items() for d in x['predecesores'])
assert 'bitácora de lectura' in P['PR-01']['entregable'] and 'restauración' in P['PR-02']['entregable']
md(OUT/'PF07_validacion.txt','''VALIDACIÓN DEL ESCENARIO
1. 12/12 proyectos con objetivo propuesto; 5/5 objetivos propuestos cubiertos.
2. C-13 y C-14 fusionados. Se verificó que PR-01 conserva bitácora de lectura y PR-02 incluye restauración.
3. 12/12 TCO incluyen cinco años de costo anual y salida. Los tres casos corresponden a los mayores TCO.
4. Orden topológico calculado sin ciclos y verificado para todos los predecesores.
5. Comparación histórica reconciliada con las partidas del presupuesto. El filtro de pagos no se usa como imputación al no haber conciliación por centro de costo.
Pendiente: sustituir trazabilidad provisional por la matriz PETI aprobada, validar BIA/alcance regulatorio, obtener cotizaciones y aprobar capacidad y financiación.
''')
tot=sum(z['tco_5'] for z in t);inv=sum(z['inversion_inicial'] for z in t)
sections=[
('7.1.1 Fuentes admisibles y control de admisión',
 'Se reconstruyeron las cinco fuentes del método de la Semana 13 con hechos de la empresa 04: normativa (4.1.5), arquitectura (5.4.2), capacidad (4.3.5), FODA cruzado (3.5) y servicio digital (6.1.7). Las referencias son secciones destino, no matrices del equipo ya aprobadas. 16 candidatos: 12 admitidos, 2 fusionados y 2 retirados. La bitácora de lectura queda en PR-01 y la prueba de recuperación en PR-02. Se retiraron los drones y el reemplazo del core por falta de sustento.'),
('7.1.2 Portafolio de proyectos','Los doce proyectos se detallan en PF01. Cada uno cita una fuente, un hecho y un objetivo propuesto. Se recomienda iniciar la gobernanza auditable y reservar la expansión del canal a los hitos de identidad, expedientes e integración.'),
('7.1.3 Fichas de proyecto','PF03 contiene doce fichas de veinte campos con alcance, exclusiones, responsable propuesto, plazo, dependencias, estimaciones y aceptación medible. No se han asignado nombres ni fechas de contratación.'),
('7.1.4 Costo total de propiedad',f'La inversión inicial estimada es {money(inv)}; el TCO nominal de cinco años es {money(tot)} ({tot/inv:.2f} veces la inversión). Incluye implementación, migración, integración, capacitación, operación anual y salida. Los repartos son paramétricos, contrastados con las partidas históricas y los expedientes, y no son cotizaciones. El filtro Servicio informático identifica {b["pagos"]:,} pagos por {money(b["pagos_ti"])}; supera el presupuesto TI anual y no está conciliado por centro de costo. No se traslada al TCO.'),
('7.1.5 Casos de negocio','PR-01, PR-02 y PR-08 tienen los mayores TCO. Para cada uno se comparó mantener la situación, solución mínima y solución completa. La opción completa obtiene el menor costo económico en los supuestos base, pero depende de validar la exposición y la eficacia. Las inversiones históricas no registran beneficios medidos (0 de 3). Se propone revisión a los 90 y 180 días.'),
('7.1.6 Balance del portafolio',f'El plan histórico asigna {100*b["plan"][0]/sum(b["plan"]):.1f} % a operación y {100*b["plan"][1]/sum(b["plan"]):.1f} % a inversión sin desagregar. El ejecutado registra {100*b["actual"][0]/sum(b["actual"]):.1f} % y {100*b["actual"][1]/sum(b["actual"]):.1f} %, respectivamente. La inversión inicial propuesta se distribuye 59 % operar, 25 % crecer y 16 % transformar, dentro de los intervalos orientativos 50–70 %, 20–30 % y 10–20 %. Son bases distintas: gasto histórico anual frente a proyectos acumulados. No se infiere que la propuesta esté financiada; debe escalonarse.'),
('7.1.7 Dependencias','El orden topológico es '+ ' → '.join(order)+'. Las olas indican precedencia técnica, no un cronograma financiado. PR-03 habilita seguridad e inventario; PR-04 y PR-05 preceden integración y expedientes. PR-01 y PR-09 habilitan el autoservicio PR-08.'),
('7.1.8 Cobertura de objetivos','Los cinco objetivos propuestos tienen al menos un proyecto. La cobertura de la sección 6.2 aprobada sigue pendiente porque esa sección no se entregó.'),
]
lines=['# 7.1 Portafolio de proyectos','COOPAC Frontera Sur · Grupo 4 · escenario académico sujeto a validación.']
for title,txt in sections:
    lines+=['\n## '+title,txt]
    if title.startswith('7.1.2'):
        lines+=['\n| Código | Proyecto | Fuente PETI | Objetivo | Categoría |','|---|---|---|---|---|']
        lines += [f"| [{c}](PF03_fichas/{c}.md) | {x['proyecto']} | {x['fuente']} · {x['seccion_origen']} | {x['objetivo']} | {x['categoria']} |" for c,x in P.items()]
    if title.startswith('7.1.4'):
        lines+=['\n| Código | Inversión | Operación anual | TCO 5 años | Factor | Rango |','|---|---:|---:|---:|---:|---|']
        lines += [f"| {z['codigo']} | {money(z['inversion_inicial'])} | {money(z['costo_anual'])} | {money(z['tco_5'])} | {z['factor']:.2f}× | {money(z['tco_min'])} a {money(z['tco_max'])} |" for z in t]
        high=sorted(t,key=lambda z:-z['operacion_pct'])[:3]
        lines+=['\nMayor proporción recurrente: '+', '.join(f"{z['codigo']} ({z['operacion_pct']} %)" for z in high)+'.']
    if title.startswith('7.1.5'):lines+=['\n- ['+c+' · caso completo](PF04_casos/'+c+'.md)' for c in cases]
    if title.startswith('7.1.8'):lines+=['\n- '+k+': '+OBJ[k]+' Proyectos: '+', '.join(coverage[k])+'.' for k in OBJ]
lines+=['\n## Nota sobre alcance regulatorio','La ficha del caso menciona SBS 504-2021. Para la matriz 4.1.5, revisar además la norma sectorial COOPAC y confirmar nivel y alcance; no se infiere plazo legal ni cumplimiento formal. Referencia: [SBS, Resolución 1297-2022](https://www.sbs.gob.pe/Portals/1/jer/Ley_COOPAC_Normas_Regulatorias/Res.%201297-2022.pdf).']
md(HERE/'7.1_portafolio.md','\n\n'.join(lines[:2])+'\n'+'\n'.join(lines[2:]))
md(HERE/'README.md','''# Portafolio de la Semana 13
COOPAC Frontera Sur · Grupo 4. Los CSV originales y los programas de ejemplo en la raíz se conservan.

Ejecutar desde la raíz con Python 3.10+ y matplotlib:

    python -m pip install matplotlib
    python 07_portafolio/generar.py

Los scripts PF01, PF02, PF04, PF05 y PF06 se pueden ejecutar por separado en ese orden. El generador también escribe las fichas, casos, sección 7.1 y salidas bajo evidencias/S13. Los montos son nominales y académicos. La fuente normativa y la cobertura de objetivos son provisionales hasta contrastar las secciones previas del PETI.
''')
(HERE/'resumen.json').write_text(json.dumps(dict(portafolio=list(P.values()),tco=t,casos=cases,
  presupuesto=b,orden=order,cobertura=coverage,objetivos=OBJ,secciones=sections,fichas=fichas),ensure_ascii=False,indent=2),encoding='utf-8')
print(f'12 proyectos, {len(fichas)} fichas, {len(cases)} casos. Inversión {money(inv)}; TCO {money(tot)}.')
