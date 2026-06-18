// ═══════════════════════════════════════════════════════════════
//  AGROVIP S.A. — ARCHIVO DE DATOS SEMANAL
//  Actualizar cada jueves en GitHub:
//  1. Clic en datos.js → ícono lápiz ✏ → editar
//  2. Cambiar valores de "semana" y agregar fila al historial
//  3. Clic "Commit changes" → listo en 60 segundos
// ═══════════════════════════════════════════════════════════════

const DATOS = {

  // ┌─────────────────────────────────────────────────────────┐
  // │  EDITAR ESTO CADA JUEVES                                │
  // └─────────────────────────────────────────────────────────┘
  semana: {
    numero:      22,
    periodo:     "22–28 Mayo 2026",
    actualizado: "22 May 2026",

    // --- PRECIOS AL PRODUCTOR ---
    precio_productor:     0.95,   // $/kg pagado al productor
    precio_productor_ant: 2.30,   // $/kg semana anterior

    // --- USDA (consultar cada jueves) ---
    usda_ny:   36.00,   // NX_FV010 → caja 4.5kg Ecuador roja/blanca NY
    usda_la:   17.50,   // HC_FV056 → caja 10lb Ecuador bote LA
    usda_fob:  26.00,   // FVDFOB   → FOB Ecuador 4.5kg

    // --- PRECIOS RETAIL POR CADENA (actualizar cada jueves) ---
    retail: {
      walmart:        { precio_unidad: 4.97, kg_equiv: 12.4, url: "https://www.walmart.com/ip/Fresh-Dragon-Fruit-Each/638705858" },
      publix:         { precio_unidad: 5.53, kg_equiv: 13.8, oferta: 4.41, oferta_pct: 20, url: "https://www.publix.com/pd/dragon-fruit/RIO-PCI-107583" },
      sprouts:        { precio_unidad: 4.99, kg_equiv: 12.5, url: "https://shop.sprouts.com/store/sprouts/products/16346073-dragonfruit-pitaya-each" },
      whole_foods:    { precio_unidad: 5.49, kg_equiv: 13.7, url: "https://www.wholefoodsmarket.com/product/produce-dragon-fruit-b07fzct282" },
      whole_foods_lb: { precio_lb: 6.99,    kg_equiv: 15.4, nota: "Orgánico por peso", url: "https://www.wholefoodsmarket.com/product/produce-dragon-fruit-b07fzct282" },
      kroger:         { precio_unidad: 4.97, kg_equiv: 12.4, url: "https://www.kroger.com/p/white-dragon-fruit/0000000003040" },
    },

    // --- MERCADO ---
    tendencia:      "baja",   // "baja" | "estable" | "alza" | "incierta"
    oferta_ecuador: "alta",   // "alta" | "media" | "baja"

    // --- COMPETIDORES EN PERCHA ---
    mango:       true,
    fresas:      true,
    blueberries: true,
    cerezas:     true,
    lichi:       true,
    uvas:        false,

    // --- NOTA PARA PRODUCTORES ---
    nota: "Mayo–junio es el período de mayor competencia del año. Mango México en pico absoluto, cerezas California con cosecha récord adelantada 7–10 días, fresas en plena temporada y lichi entrando en la Costa Oeste. La fruta comprada esta semana llega a la percha el 11–12 de junio.",

    // --- PROYECCIÓN PRÓXIMAS 2 SEMANAS ---
    proyeccion: [
      { sem: 23, periodo: "29 May–4 Jun", prod: 0.85, usda_la: 16.50, dir: "baja", razon: "Mango + cerezas + lichi en volumen máximo." },
      { sem: 24, periodo: "5–11 Jun",     prod: 0.80, usda_la: 16.00, dir: "baja", razon: "Presión máxima. Fruta sem 22 llega a LA." }
    ]
  },

  // ┌─────────────────────────────────────────────────────────┐
  // │  HISTORIAL — agregar UNA fila nueva cada jueves         │
  // └─────────────────────────────────────────────────────────┘
  historial: [
    { sem:22, periodo:"22–28 May 2026", prod:0.95, ny:36.0, la:17.5, tend:"baja",  comps:["mango","fresas","blueberries","cerezas","lichi"],
      retail_avg: 13.0 },
    { sem:21, periodo:"12–18 May 2026", prod:2.30, ny:38.0, la:17.5, tend:"baja",  comps:["mango","fresas"],
      retail_avg: 13.2 },
    { sem:20, periodo:"5–11 May 2026",  prod:2.80, ny:45.0, la:19.0, tend:"alza",  comps:["mango"],
      retail_avg: 13.8 },
  ],

  // ┌─────────────────────────────────────────────────────────┐
  // │  CONFIGURACIÓN FIJA — solo cambia si cambian costos     │
  // └─────────────────────────────────────────────────────────┘
  config: {
    flete_mar:  1.74,    // $/kg Guayaquil → Miami
    flete_cam:  0.50,    // $/kg Miami → LA (camión 2 días)
    flete_sf:   0.65,    // $/kg Miami → SF
    margen:     0.14,    // margen Agrovip 14%
    kg_cont:    17280,   // kg netos por contenedor
    peso_unidad: 0.40,   // kg promedio por unidad en retail

    // Cadena de márgenes por eslabón
    margenes_cadena: {
      exportador:   0.65,
      importador:   0.22,
      distribuidor: 0.19,
      supermercado: 0.34,
    }
  }
};
