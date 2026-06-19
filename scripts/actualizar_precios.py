"""
Agrovip S.A. — Script de actualización automática de precios USDA
Se ejecuta cada jueves vía GitHub Actions
Llama a la API MARS de USDA y actualiza datos.js automáticamente
"""

import os
import json
import requests
import datetime
import re

# ── CONFIGURACIÓN ──────────────────────────────────────────────
API_KEY       = os.environ.get('USDA_API_KEY', '')
PRECIO_PROD   = float(os.environ.get('PRECIO_PRODUCTOR', '0.00'))
BASE_URL      = 'https://marsapi.ams.usda.gov/services/v1.2'
DATOS_FILE    = 'datos.js'

# Códigos de reporte USDA para pitahaya
REPORTS = {
    'ny':  'NX_FV010',   # Terminal NY
    'la':  'HC_FV056',   # Terminal LA
    'fob': 'FVDFOB',     # FOB Nacional
}

# Precios retail fijos (se actualizan manualmente cuando cambian)
RETAIL_FIJO = {
    'walmart':        {'precio_unidad': 4.97, 'kg_equiv': 12.4, 'url': 'https://www.walmart.com/ip/Fresh-Dragon-Fruit-Each/638705858'},
    'publix':         {'precio_unidad': 5.53, 'kg_equiv': 13.8, 'oferta': 4.41, 'oferta_pct': 20, 'url': 'https://www.publix.com/pd/dragon-fruit/RIO-PCI-107583'},
    'sprouts':        {'precio_unidad': 4.99, 'kg_equiv': 12.5, 'url': 'https://shop.sprouts.com/store/sprouts/products/16346073-dragonfruit-pitaya-each'},
    'whole_foods':    {'precio_unidad': 5.49, 'kg_equiv': 13.7, 'url': 'https://www.wholefoodsmarket.com/product/produce-dragon-fruit-b07fzct282'},
    'whole_foods_lb': {'precio_lb': 6.99,    'kg_equiv': 15.4, 'nota': 'Orgánico por peso', 'url': 'https://www.wholefoodsmarket.com/product/produce-dragon-fruit-b07fzct282'},
    'kroger':         {'precio_unidad': 4.97, 'kg_equiv': 12.4, 'url': 'https://www.kroger.com/p/white-dragon-fruit/0000000003040'},
}

# Competidores por mes
COMPETIDORES_POR_MES = {
    1:  {'mango': False, 'fresas': False, 'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
    2:  {'mango': False, 'fresas': False, 'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
    3:  {'mango': False, 'fresas': True,  'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
    4:  {'mango': True,  'fresas': True,  'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
    5:  {'mango': True,  'fresas': True,  'blueberries': True,  'cerezas': True,  'lichi': True,  'uvas': False},
    6:  {'mango': True,  'fresas': True,  'blueberries': True,  'cerezas': True,  'lichi': True,  'uvas': False},
    7:  {'mango': True,  'fresas': False, 'blueberries': True,  'cerezas': False, 'lichi': True,  'uvas': True},
    8:  {'mango': True,  'fresas': False, 'blueberries': True,  'cerezas': False, 'lichi': False, 'uvas': True},
    9:  {'mango': False, 'fresas': False, 'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': True},
    10: {'mango': False, 'fresas': False, 'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
    11: {'mango': False, 'fresas': False, 'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
    12: {'mango': False, 'fresas': False, 'blueberries': False, 'cerezas': False, 'lichi': False, 'uvas': False},
}

def get_week_number():
    return datetime.date.today().isocalendar()[1]

def get_periodo():
    today = datetime.date.today()
    # Inicio de semana (lunes)
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    return f"{monday.day}–{sunday.day} {meses[sunday.month-1]} {sunday.year}"

def fetch_usda_report(slug, keyword='DRAGON FRUIT'):
    """Llama a la API MARS y extrae precio de pitahaya Ecuador"""
    headers = {'Authorization': f'Basic {API_KEY}'}
    try:
        # Obtener datos del reporte
        url = f"{BASE_URL}/reports/{slug}?q={keyword}&allSections=true"
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"  ⚠ {slug}: HTTP {r.status_code}")
            return None
        data = r.json()

        # Buscar entradas de Ecuador pitahaya
        results = data.get('results', [])
        ecuador_prices = []
        for item in results:
            commodity = str(item.get('commodity', '')).upper()
            origin    = str(item.get('origin', '')).upper()
            variety   = str(item.get('variety', '')).upper()
            unit_desc = str(item.get('unit_desc', '')).lower()

            is_dragon = 'DRAGON' in commodity or 'PITAH' in commodity
            is_ecuador = 'ECUADOR' in origin or 'ECUADOR' in variety
            is_fresh   = 'frozen' not in commodity.lower()

            if is_dragon and is_ecuador and is_fresh:
                price_low  = item.get('price_low')
                price_high = item.get('price_high')
                if price_low and price_high:
                    avg = (float(price_low) + float(price_high)) / 2
                    ecuador_prices.append({
                        'avg': avg,
                        'low': float(price_low),
                        'high': float(price_high),
                        'unit': unit_desc,
                        'variety': variety
                    })
                    print(f"  ✅ {slug}: ${price_low}–${price_high} ({unit_desc})")

        if ecuador_prices:
            # Priorizar caja 4.5kg o 10lb
            for p in ecuador_prices:
                if '4.5' in p['unit'] or '10' in p['unit']:
                    return p['avg']
            return ecuador_prices[0]['avg']

        print(f"  ⚠ {slug}: Sin datos Ecuador esta semana")
        return None

    except Exception as e:
        print(f"  ❌ {slug}: Error — {e}")
        return None

def load_existing_datos():
    """Carga el datos.js actual para preservar historial"""
    try:
        with open(DATOS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        # Extraer historial actual
        match = re.search(r'historial:\s*\[(.*?)\],', content, re.DOTALL)
        if match:
            return content, match.group(0)
    except:
        pass
    return None, None

def extract_historial(content):
    """Extrae el array historial del JS"""
    match = re.search(r'historial:\s*(\[.*?\]),', content, re.DOTALL)
    if match:
        # Limpiar para parsear como JSON
        hist_str = match.group(1)
        # Reemplazar JS con JSON válido
        hist_str = re.sub(r'//.*?\n', '\n', hist_str)
        try:
            return json.loads(hist_str)
        except:
            pass
    return []

def extract_precio_productor_ant(content):
    """Extrae precio productor de semana anterior del datos.js"""
    match = re.search(r'precio_productor:\s*([\d.]+)', content)
    if match:
        return float(match.group(1))
    return 0.0

def get_tendencia(ny_price, la_price, historial):
    """Calcula tendencia basada en histórico"""
    if not historial or len(historial) < 2:
        return 'incierta'
    prev_ny = historial[0].get('ny', 0)
    if ny_price and prev_ny:
        diff = ny_price - prev_ny
        if diff < -2:   return 'baja'
        elif diff > 2:  return 'alza'
        else:           return 'estable'
    return 'incierta'

def get_oferta_ecuador(month):
    """Determina nivel de oferta Ecuador por mes"""
    pico = [3, 4, 5, 9, 10]  # Meses pico en Ecuador
    baja = [7, 8, 12, 1]
    if month in pico: return 'alta'
    if month in baja: return 'baja'
    return 'media'

def calcular_proyeccion(prod, la_price, semana, month):
    """Calcula proyección 2 semanas basada en estacionalidad"""
    seasonal = {
        5: -1.5, 6: -1.5, 7: -1.0,
        8: -0.5, 9: 0.2,  10: 0.5,
        11: 0.3, 12: 0.0, 1: 0.2, 2: 0.3, 3: 0.5, 4: 0.0
    }
    adj = seasonal.get(month, 0)
    la1 = round(max(12, la_price + adj), 2) if la_price else None
    la2 = round(max(12, la_price + adj * 1.3), 2) if la_price else None

    def max_prod(la):
        if not la: return prod
        kg = la / 4.536
        fob = kg - 1.74 - 0.50
        return round(max(0, fob / 1.65), 2)

    p1 = max_prod(la1)
    p2 = max_prod(la2)

    dir1 = 'baja' if p1 < prod else ('alza' if p1 > prod else 'estable')
    dir2 = 'baja' if p2 < p1  else ('alza' if p2 > p1  else 'estable')

    meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    s1_name = f"Sem {semana+1}"
    s2_name = f"Sem {semana+2}"

    razones = {
        'baja': 'Presión estacional continúa.',
        'alza': 'Menor competencia estacional.',
        'estable': 'Mercado estable a corto plazo.'
    }

    return [
        {'sem': semana+1, 'periodo': s1_name, 'prod': p1,
         'usda_la': la1, 'dir': dir1, 'razon': razones[dir1]},
        {'sem': semana+2, 'periodo': s2_name, 'prod': p2,
         'usda_la': la2, 'dir': dir2, 'razon': razones[dir2]},
    ]

def generar_datos_js(semana, periodo, precio_prod, precio_prod_ant,
                     ny, la, fob, tendencia, oferta, comps,
                     proyeccion, historial_js, retail):
    """Genera el contenido completo de datos.js"""

    comps_js = '\n'.join([
        f"    {k}: {'true' if v else 'false'},"
        for k, v in comps.items()
    ])

    proy_js = ',\n      '.join([
        f"{{ sem: {p['sem']}, periodo: \"{p['periodo']}\", prod: {p['prod']}, "
        f"usda_la: {p['usda_la']}, dir: \"{p['dir']}\", razon: \"{p['razon']}\" }}"
        for p in proyeccion
    ])

    hist_rows = ',\n    '.join([
        f"{{ sem:{h['sem']}, periodo:\"{h['periodo']}\", "
        f"prod:{h['prod']}, ny:{h.get('ny','null')}, la:{h.get('la','null')}, "
        f"tend:\"{h.get('tend','estable')}\", "
        f"comps:{json.dumps(h.get('comps',[]))}, "
        f"retail_avg:{h.get('retail_avg', 13.0)} }}"
        for h in historial_js
    ])

    retail_js_str = json.dumps(retail, indent=6, ensure_ascii=False)

    today = datetime.date.today()
    meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    fecha_hoy = f"{today.day} {meses[today.month-1]} {today.year}"

    nota = generar_nota(comps, tendencia, la)

    ny_str  = str(round(ny, 1))  if ny  else 'null'
    la_str  = str(round(la, 2))  if la  else 'null'
    fob_str = str(round(fob, 1)) if fob else 'null'

    return f"""// ═══════════════════════════════════════════════════════════════
//  AGROVIP S.A. — DATOS DE MERCADO
//  Actualizado automáticamente cada jueves por GitHub Actions
//  Última actualización: {fecha_hoy}
//  ⚠ No editar manualmente — se sobreescribe cada jueves
// ═══════════════════════════════════════════════════════════════

const DATOS = {{

  semana: {{
    numero:      {semana},
    periodo:     "{periodo}",
    actualizado: "{fecha_hoy}",

    precio_productor:     {precio_prod},
    precio_productor_ant: {precio_prod_ant},

    walmart: {retail.get('walmart', {}).get('precio_unidad', 4.97)},

    usda_ny:  {ny_str},
    usda_la:  {la_str},
    usda_fob: {fob_str},

    retail: {retail_js_str},

    tendencia:      "{tendencia}",
    oferta_ecuador: "{oferta}",

{comps_js}

    nota: "{nota}",

    proyeccion: [
      {proy_js}
    ]
  }},

  historial: [
    {hist_rows}
  ],

  config: {{
    flete_mar:   1.74,
    flete_cam:   0.50,
    flete_sf:    0.65,
    margen:      0.14,
    kg_cont:     17280,
    peso_unidad: 0.40,
    margenes_cadena: {{
      exportador:   0.65,
      importador:   0.22,
      distribuidor: 0.19,
      supermercado: 0.34
    }}
  }}
}};
"""

def generar_nota(comps, tendencia, la_price):
    activos = [k for k, v in comps.items() if v]
    nombres = {'mango':'Mango México','fresas':'Fresas California',
               'blueberries':'Blueberries','cerezas':'Cerezas California',
               'lichi':'Lichi','uvas':'Uvas California'}
    nombres_activos = [nombres.get(k, k) for k in activos]
    if not nombres_activos:
        return "Menor competencia estacional esta semana. Mejor posición para pitahaya en percha."
    return (f"Esta semana hay {len(activos)} competidores activos en percha: "
            f"{', '.join(nombres_activos)}. La pitahaya compite por espacio limitado "
            f"en la sección de produce de los supermercados.")

def main():
    print("=" * 60)
    print("AGROVIP — Actualización automática de precios USDA")
    print(f"Fecha: {datetime.date.today()}")
    print("=" * 60)

    today    = datetime.date.today()
    semana   = int(os.environ.get('SEMANA_NUMERO', '') or get_week_number())
    periodo  = get_periodo()
    month    = today.month

    print(f"\n📅 Semana {semana} · {periodo}")
    print(f"💵 Precio productor ingresado: ${PRECIO_PROD}/kg")

    # Cargar datos existentes
    content, _ = load_existing_datos()
    historial_existente = extract_historial(content) if content else []
    precio_prod_ant = extract_precio_productor_ant(content) if content else 0.0

    print(f"\n📊 Consultando API USDA MARS...")
    ny_price  = fetch_usda_report(REPORTS['ny'])
    la_price  = fetch_usda_report(REPORTS['la'])
    fob_price = fetch_usda_report(REPORTS['fob'])

    # Fallback si API no devuelve datos
    if not ny_price:
        print("  ⚠ NY sin datos — usando último valor conocido")
        ny_price = next((h['ny'] for h in historial_existente if h.get('ny')), 36.0)
    if not la_price:
        print("  ⚠ LA sin datos — usando último valor conocido")
        la_price = next((h['la'] for h in historial_existente if h.get('la')), 17.5)
    if not fob_price:
        fob_price = next((h.get('fob') for h in historial_existente if h.get('fob')), 26.0)

    print(f"\n✅ Precios obtenidos:")
    print(f"   USDA NY:  ${ny_price}/caja")
    print(f"   USDA LA:  ${la_price}/caja")
    print(f"   FOB:      ${fob_price}/caja")

    tendencia = get_tendencia(ny_price, la_price, historial_existente)
    oferta    = get_oferta_ecuador(month)
    comps     = COMPETIDORES_POR_MES.get(month, {})
    proyeccion = calcular_proyeccion(PRECIO_PROD, la_price, semana, month)

    # Actualizar historial
    retail_avg = round(sum([
        RETAIL_FIJO['walmart']['kg_equiv'],
        RETAIL_FIJO['publix']['kg_equiv'],
        RETAIL_FIJO['sprouts']['kg_equiv'],
        RETAIL_FIJO['whole_foods']['kg_equiv'],
    ]) / 4, 1)

    nueva_entrada = {
        'sem': semana, 'periodo': periodo,
        'prod': PRECIO_PROD, 'ny': ny_price, 'la': la_price,
        'tend': tendencia,
        'comps': [k for k, v in comps.items() if v],
        'retail_avg': retail_avg
    }

    # Evitar duplicar semana actual
    historial_nuevo = [h for h in historial_existente if h.get('sem') != semana]
    historial_nuevo.insert(0, nueva_entrada)
    historial_nuevo = historial_nuevo[:52]  # Máximo 1 año de historial

    # Generar datos.js
    nuevo_js = generar_datos_js(
        semana=semana, periodo=periodo,
        precio_prod=PRECIO_PROD, precio_prod_ant=precio_prod_ant,
        ny=ny_price, la=la_price, fob=fob_price,
        tendencia=tendencia, oferta=oferta, comps=comps,
        proyeccion=proyeccion, historial_js=historial_nuevo,
        retail=RETAIL_FIJO
    )

    with open(DATOS_FILE, 'w', encoding='utf-8') as f:
        f.write(nuevo_js)

    print(f"\n✅ datos.js actualizado exitosamente")
    print(f"   Semana: {semana} · Tendencia: {tendencia} · Oferta EC: {oferta}")
    print(f"   Competidores: {[k for k,v in comps.items() if v]}")
    print(f"   Proyección +1: ${proyeccion[0]['prod']}/kg · +2: ${proyeccion[1]['prod']}/kg")
    print("\n🚀 Listo para commit en GitHub")

if __name__ == '__main__':
    main()
