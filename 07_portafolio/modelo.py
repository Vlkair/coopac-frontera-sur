"""Escenario académico Grupo 4. Montos en soles nominales; no son cotizaciones."""
from pathlib import Path
import csv, json, graphlib
from decimal import Decimal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G = ROOT/'graficos'
O = 'Operar'
C = 'Crecer'
T = 'Transformar'
FUENTES = {'N': ('Obligación normativa', '4.1.5'), 'A': ('Brecha de arquitectura','5.4.2'),
           'P': ('Brecha de capacidad','4.3.5'), 'F': ('FODA cruzado','3.5'),
           'S': ('Brecha de servicio digital','6.1.7')}
OBJ = {
 'OE-01':'Proteger expedientes: 100 % de lecturas auditadas en el piloto y cero accesos indebidos en pruebas de aceptación.',
 'OE-02':'Recuperar servicios críticos: dos simulacros por año con RTO ≤ 8 h y RPO ≤ 4 h, metas sujetas a aprobación del BIA.',
 'OE-03':'Asegurar operación TI: ≥ 90 % de cambios críticos aprobados antes del despliegue y 100 % de contratos críticos con aviso.',
 'OE-04':'Extender autoservicio: ≥ 60 % de solicitudes elegibles del piloto terminadas sin acudir a agencia.',
 'OE-05':'Demostrar valor: 100 % de proyectos nuevos con revisión de beneficios a los 90 y 180 días.'}
# nombre, clase, fuente, objetivo, inversión inicial (miles), operación anual (miles),
# salida (miles), margen %, meses, responsable propuesto, hecho, entregable, aceptación, predecesores
DATA = [
 ('Expedientes de crédito trazables',O,'A','OE-01',180,42,10,35,8,'Créditos y TI','Ficha C y G: carpetas sin auditoría; 1 900 expedientes accedidos indebidamente','Repositorio con permisos por rol, migración piloto, bitácora de lectura y alertas','100 % de lecturas piloto trazadas; pruebas de permisos sin accesos indebidos',(4,5)),
 ('Continuidad y recuperación verificable',O,'A','OE-02',145,36,10,35,7,'TI y Riesgos','Ficha E, F y H: respaldo conectado y plan sin pruebas; INV03 no midió resultado','Copias aisladas, BIA revisado, restauración y simulacro con acta','Dos pruebas al año; RTO ≤ 8 h y RPO ≤ 4 h en piloto',(3,)),
 ('Gobierno de seguridad auditable',O,'N','OE-01',80,18,4,30,5,'Oficial de Seguridad y Riesgos','Ficha B, C y H: documento de seguridad sin implantar; validar alcance SBS','Matriz normativa, política, roles, riesgos y repositorio de evidencias','Política aprobada y todos los riesgos críticos con dueño y tratamiento',()),
 ('Identidad y segundo factor',O,'A','OE-01',65,14,4,30,4,'TI y Seguridad','Ficha F: segundo factor disponible y no habilitado; política de contraseñas ausente','Segundo factor, baja de cuentas y revisión de roles','100 % de cuentas privilegiadas del piloto con segundo factor probado',(3,)),
 ('Inventario y clasificación de activos',O,'P','OE-01',45,9,2,30,3,'TI y dueños de datos','Ficha F: no existe inventario de activos TI','Inventario con dueño, criticidad y clasificación','100 % de activos críticos del piloto inventariados y revisados',(3,)),
 ('Mesa de incidentes y cambios',O,'P','OE-03',40,9,2,30,4,'Operaciones TI','Ficha F: incidentes sin registro y cambios documentados después de aplicar','Flujos de tickets, escalamiento y aprobación previa','≥ 90 % de cambios críticos con autorización previa en el piloto',(5,)),
 ('Gestión de contratos y SLA',O,'P','OE-03',35,8,2,25,3,'Administración y TI','Ficha F: no se controlan vencimientos; Ficha C: contrato SLA del core','Registro, alertas de vencimiento y revisión trimestral','100 % de contratos críticos registrados con responsable y alerta',()),
 ('Autoservicio de solicitudes al socio',C,'S','OE-04',140,32,10,40,8,'Atención al Socio y TI','Ficha C y D: canal web existente y atención en agencias; recorrido remoto no acreditado','Piloto de solicitud y seguimiento digital integrado al canal existente','≥ 60 % de trámites elegibles del piloto se completan en línea',(1,9)),
 ('Integración segura de canales',C,'A','OE-04',65,14,4,35,5,'Arquitectura TI','Ficha C: core, canal web y bureau separados; inventario de interfaces pendiente','Inventario de interfaces, intercambio autenticado y pruebas de conciliación','100 % de interfaces piloto con trazabilidad y prueba de recuperación',(4,5)),
 ('Adopción asistida en agencias',C,'F','OE-04',45,8,2,30,4,'Atención al Socio','Ficha A y D: 21 400 socios y agencias en Tacna y valles; hipótesis FO de extender canal existente','Material accesible, formación y ayuda en agencias piloto','≥ 80 % del personal piloto completa práctica; se mide adopción por agencia',(8,)),
 ('Gobierno de datos y beneficios',T,'F','OE-05',95,16,5,35,6,'Finanzas y Comité TI','Expedientes e inversiones: 0 de 3 inversiones con beneficio medido; hipótesis DO','Registro de inversiones, catálogo de métricas y revisiones a 90 y 180 días','100 % de proyectos nuevos con indicador, dueño y revisión programada',()),
 ('Piloto de alertas operativas',T,'F','OE-01',65,14,4,40,5,'Riesgos y Seguridad','Ficha G: detección por denuncia; oportunidad de alertar con la nueva bitácora','Reglas de detección y revisión humana de alertas, sin decisiones automáticas','100 % de accesos anómalos de prueba generan alerta investigable',(1,11)),
]
P = {}
for i,row in enumerate(DATA,1):
    name,cat,src,obj,initial,annual,exit_,margin,months,owner,fact,deliver,metric,deps=row
    code=f'PR-{i:02}'
    P[code]=dict(codigo=code, proyecto=name,categoria=cat,fuente=FUENTES[src][0],
        seccion_origen=FUENTES[src][1],objetivo=obj,evidencia=fact,entregable=deliver,
        criterio=metric,responsable=owner,meses=months,predecesores=[f'PR-{d:02}' for d in deps],
        inicial=initial*1000,anual=annual*1000,salida=exit_*1000,margen_pct=margin)

def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def save(name,rows):
    with (HERE/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def md(path,s):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(s.strip()+'\n',encoding='utf-8')

def money(n):return f'S/ {n:,.2f}'.translate(str.maketrans({',':' ','.':','}))

def consolidar():
    out=[]
    for x in P.values():
        assert x['objetivo'] in OBJ and x['fuente'] in {a for a,b in FUENTES.values()}
        out.append({k:x[k] for k in ['codigo','proyecto','fuente','seccion_origen','objetivo','categoria','evidencia','entregable','criterio']})
    save('PF01_portafolio_candidatos.csv',out)
    save('PF01_control_admision.csv',[
      dict(candidato='C-13 Registro de lecturas',decision='Fusionado en PR-01',razon='El registro, conservación y alerta de lecturas se mantienen como entregables del expediente trazable.'),
      dict(candidato='C-14 Prueba de restauración',decision='Fusionado en PR-02',razon='El ensayo de restauración se conserva como aceptación del alcance de continuidad.'),
      dict(candidato='C-15 Compra de drones',decision='Retirado',razon='Sin fuente admisible ni objetivo del caso.'),
      dict(candidato='C-16 Sustituir core financiero',decision='Retirado',razon='Core con soporte; no se acreditó una brecha que justifique reemplazo.')])
    print('16 candidatos: 12 admitidos, 2 fusionados, 2 retirados. Cinco fuentes reconstruidas; aprobación PETI pendiente.')
    for x in out:print(x['codigo'],x['objetivo'],x['seccion_origen'],x['proyecto'])

def tco():
    out=[]
    for x in P.values():
        # Repartos paramétricos académicos; no representan partidas cotizadas.
        i,a,s,m=(x[k] for k in ('inicial','anual','salida','margen_pct'))
        impl=i*60//100;cap=i*10//100; mig=i*10//100
        lic=a*25//100;infra=a*15//100;sop=a*35//100;pers=a*20//100
        total=i+5*a+s
        out.append(dict(codigo=x['codigo'],implementacion=impl,capacitacion_inicial=cap,migracion=mig,
          integracion=i-impl-cap-mig,inversion_inicial=i,licencias_anual=lic,infra_anual=infra,
          soporte_anual=sop,personal_anual=pers,capacitacion_anual=a-lic-infra-sop-pers,
          costo_anual=a,salida_ano_5=s,tco_5=total,factor=round(total/i,2),
          operacion_pct=round(500*a/total,1),margen_pct=m,tco_min=round(total*(100-m)/100),
          tco_max=round(total*(100+m)/100),referencia=(
              'INV03 y PT03/PT07' if x['codigo']=='PR-02' else
              'INV02 y PT06; comparar alcance' if x['codigo'] in ('PR-01','PR-08') else
              'PT01/PT02/PT05/PT07; orden de magnitud de alcance, validar cotización')))
    out.sort(key=lambda z:-z['tco_5'])
    save('PF02_tco.csv',out)
    for r in out:print(r['codigo'],money(r['tco_5']),f"{r['factor']}×",money(r['tco_min']),money(r['tco_max']))
    print('Inversión:',money(sum(z['inversion_inicial'] for z in out)),'TCO:',money(sum(z['tco_5'] for z in out)))
    return out

# costo anual de inacción, alternativa mínima (inicial, anual, salida), reducción mínima/completa.
CASES = {'PR-01':(120000,(90000,19000,5000),.45,.90,'2 incidentes equivalentes/año × S/ 60 000 de respuesta y reproceso'),
         'PR-02':(100000,(70000,21000,5000),.45,.88,'2 interrupciones equivalentes/año × S/ 50 000 de interrupción y recuperación'),
         'PR-08':(100000,(70000,16000,5000),.40,.85,'25 000 solicitudes elegibles/año × 8 min × S/ 30 por hora de atención')}

def alternativas():
    out=[]
    for code,(base,minimum,f1,f2,driver) in CASES.items():
        x=P[code]; complete=tuple(x[k] for k in ('inicial','anual','salida'))
        for opt,(i,a,s),f in [('No hacer nada',(0,0,0),0),('Solución mínima',minimum,f1),('Solución completa',complete,f2)]:
            cost=i+5*a+s;loss=round(base*5*(1-f));avoided=base*5-loss
            out.append(dict(codigo=code,alternativa=opt,inversion_inicial=i,costo_anual=a,salida=s,
                tco_5=cost,incertidumbre_pct=x['margen_pct'],tco_min=round(cost*(100-x['margen_pct'])/100),
                tco_max=round(cost*(100+x['margen_pct'])/100),inaccion_5=base*5,
                beneficio_incremental_5=avoided,beneficio_frente_escenario_ideal_5=-loss,
                costo_economico_5=cost+loss,mejora_neta_vs_inaccion=avoided-cost,supuesto=driver))
    save('PF04_alternativas.csv',out)
    for r in out:print(r['codigo'],r['alternativa'],'TCO',money(r['tco_5']),'costo con pérdida residual',money(r['costo_economico_5']))
    return out

def balance():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    budget=read(ROOT/'presupuesto_ti.csv'); payments=read(ROOT/'pagos.csv')
    inc=read(ROOT/'inversiones_cerradas.csv')
    actual=[sum(Decimal(x['ejecutado']) for x in budget if x['tipo']==k) for k in ('Operación','Inversión')]
    plan=[sum(Decimal(x['planificado']) for x in budget if x['tipo']==k) for k in ('Operación','Inversión')]
    paid=[x for x in payments if x['concepto']=='Servicio informático' and x['estado']=='Pagado' and x['moneda']=='PEN' and x['fecha'].startswith('2025-')]
    paidtotal=sum(Decimal(x['monto']) for x in paid)
    ids={x['id_pago'] for x in paid}
    assert len(ids)==len(paid)
    new=[sum(x['inicial'] for x in P.values() if x['categoria']==k) for k in (O,C,T)]
    costs=read(HERE/'PF02_tco.csv')
    print('Histórico planificado: operar',money(plan[0]),'inversión no desagregada',money(plan[1]))
    print('Histórico ejecutado: operar',money(actual[0]),'inversión no desagregada',money(actual[1]))
    print('Pagos candidatos TI por concepto:',len(paid),money(paidtotal),'— no conciliados al presupuesto; no imputar al TCO.')
    print('Inversiones cerradas:',len(inc),'; beneficio medido:',sum(x['beneficio_medido']!='No se midió' for x in inc))
    print('Propuesta: inversión inicial por categoría',new)
    G.mkdir(exist_ok=True)
    fig,(ax,bx)=plt.subplots(1,2,figsize=(11,5),gridspec_kw={'width_ratios':[1,1.1]})
    for idx,vals in enumerate([plan,actual,new]):
        pos=0
        for n,col in zip(vals,['#275b83','#b19048'] if idx<2 else ['#275b83','#369389','#816aaa']):
            pct=float(n/sum(vals))*100
            ax.barh(idx,pct,left=pos,color=col)
            if pct>7:ax.text(pos+pct/2,idx,f'{pct:.1f}%',ha='center',va='center',color='white')
            pos+=pct
    ax.set_yticks([0,1,2],['Plan histórico','Ejecutado histórico','Inversión propuesta'])
    ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('% del total de su base');ax.set_title('Balance del portafolio')
    from matplotlib.patches import Patch
    legend=[Patch(facecolor=c,label=label) for c,label in (
        ('#275b83','Operar'),('#b19048','Inversión histórica sin desglose'),
        ('#369389','Crecer'),('#816aaa','Transformar'))]
    fig.legend(handles=legend,loc='lower center',ncol=4,frameon=False,fontsize=9)
    bx.barh([r['codigo'] for r in costs],[int(r['tco_5'])/1000 for r in costs],color='#369389')
    bx.invert_yaxis();bx.set_xlabel('Miles de soles');bx.set_title('TCO estimado a cinco años')
    fig.tight_layout(rect=(0,.08,1,1));fig.savefig(G/'PF_balance.png',dpi=160);plt.close(fig)
    return dict(actual=[float(a) for a in actual],plan=[float(a) for a in plan],new=new,
                pagos=len(paid),pagos_ti=float(paidtotal),proveedores=len({x['codigo_proveedor'] for x in paid}))

def dependencias():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    order=list(graphlib.TopologicalSorter({c:x['predecesores'] for c,x in P.items()}).static_order())
    wave={}
    for c in order:wave[c]=max((wave[d]+1 for d in P[c]['predecesores']),default=0)
    habil={d for x in P.values() for d in x['predecesores']}
    print('Orden topológico:', ' → '.join(order))
    print('Habilitadores:', ', '.join(sorted(habil)))
    fig,ax=plt.subplots(figsize=(10,4.3));coords={}
    for w in range(max(wave.values())+1):
        group=[c for c in order if wave[c]==w]
        for j,c in enumerate(group):coords[c]=(w,(len(group)-1)/2-j)
    for c,x in P.items():
        for d in x['predecesores']:
            a,b=coords[d];e,f=coords[c]
            ax.annotate('',(e-.18,f),(a+.18,b),arrowprops={'arrowstyle':'->','color':'#7692a3','lw':1.2},zorder=1)
    for c,(x,y) in coords.items():
        ax.text(x,y,c,ha='center',va='center',color='white',
                bbox={'boxstyle':'round,pad=.4','facecolor':'#275b83' if c in habil else '#369389','edgecolor':'none'},zorder=2)
    ax.set_xticks(range(max(wave.values())+1),[f'Ola {i+1}' for i in range(max(wave.values())+1)])
    ax.set_xlim(-.35,max(wave.values())+.35);ax.set_ylim(-1.6,1.6);ax.set_yticks([])
    for s in ax.spines.values():s.set_visible(False)
    ax.set_title('Dependencias del portafolio · azul: proyecto habilitador')
    fig.tight_layout();fig.savefig(G/'PF_dependencias.png',dpi=160);plt.close(fig)
    save('PF06_dependencias.csv',[dict(codigo=c,ola=wave[c]+1,predecesores='; '.join(P[c]['predecesores']),habilitador=c in habil) for c in order])
    return order,wave
