// ═══════════════════════════════════════════════════════════════
//  AGROVIP S.A. — ARCHIVO DE DATOS SEMANAL
//  ¿Cómo actualizar? → github.com/Agrovippackvip/Dragonfruitprices
//  1. Clic en datos.js → ícono lápiz (✏) → editar
//  2. Cambiar SOLO los valores de "semana_actual" y agregar
//     una fila al historial
//  3. Clic "Commit changes" → listo en 60 segundos
// ═══════════════════════════════════════════════════════════════

const DATOS = {

  // ┌─────────────────────────────────────────────────────────┐
  // │  EDITAR ESTO CADA JUEVES  (5 minutos)                   │
  // └─────────────────────────────────────────────────────────┘
  semana: {
    numero:    22,
    periodo:   "22–28 Mayo 2026",
    actualizado: "22 May 2026",

    // --- PRECIOS (consultar USDA cada jueves) ---
    precio_productor:      0.95,   // $/kg pagado al productor
    precio_productor_ant:  2.30,   // $/kg semana anterior

    usda_ny:   36.00,   // NX_FV010 → caja 4.5kg Ecuador roja/blanca NY
    usda_la:   17.50,   // HC_FV056 → caja 10lb Ecuador bote LA
    usda_fob:  26.00,   // FVDFOB   → FOB Ecuador 4.5kg
    walmart:    4.97,   // precio unitario ~400g en Walmart.com

    // --- MERCADO ---
    tendencia:      "baja",   // "baja" | "estable" | "alza" | "incierta"
    oferta_ecuador: "alta",   // "alta" | "media" | "baja"

    // --- COMPETIDORES EN PERCHA (true = activo esta semana) ---
    mango:       true,
    fresas:      true,
    blueberries: true,
    cerezas:     true,
    lichi:       true,
    uvas:        false,

    // --- NOTA PARA PRODUCTORES ---
    nota: "Mayo–junio es el período de mayor competencia del año. Mango México en pico absoluto, cerezas California con cosecha récord adelantada 7–10 días, fresas en plena temporada y lichi entrando en LA. Veritas y Mexotics están en Los Ángeles donde el USDA cotiza pitahaya Ecuador bote a $16–19 por caja de 10 lb. La fruta comprada esta semana llega a la percha el 11–12 de junio.",

    // --- PROYECCIÓN PRÓXIMAS 2 SEMANAS ---
    proyeccion: [
      { sem: 23, periodo: "29 May–4 Jun", prod: 0.85, usda_la: 16.50, dir: "baja",   razon: "Mango + cerezas + lichi en volumen máximo." },
      { sem: 24, periodo: "5–11 Jun",     prod: 0.80, usda_la: 16.00, dir: "baja",   razon: "Presión máxima. Fruta sem 22 llega a LA." }
    ]
  },

  // ┌─────────────────────────────────────────────────────────┐
  // │  HISTORIAL — agregar UNA fila nueva cada jueves         │
  // │  No borres las anteriores                               │
  // └─────────────────────────────────────────────────────────┘
  historial: [
    { sem:22, periodo:"22–28 May 2026", prod:0.95, ny:36.0, la:17.5, tend:"baja",  comps:["mango","fresas","blueberries","cerezas","lichi"] },
    { sem:21, periodo:"12–18 May 2026", prod:2.30, ny:38.0, la:17.5, tend:"baja",  comps:["mango","fresas"] },
    { sem:20, periodo:"5–11 May 2026",  prod:2.80, ny:45.0, la:19.0, tend:"alza",  comps:["mango"] },
  ],

  // ┌─────────────────────────────────────────────────────────┐
  // │  CONFIGURACIÓN FIJA — solo cambia si cambian los costos │
  // └─────────────────────────────────────────────────────────┘
  config: {
    flete_mar:   1.74,   // $/kg Guayaquil → Miami
    flete_cam:   0.50,   // $/kg Miami → LA (camión 2 días)
    margen:      0.14,   // margen Agrovip 14%
    kg_cont:     17280,  // kg netos por contenedor
    clientes: [
      { nombre:"Tierra Suelta", ciudad:"Miami, FL",        dias:10 },
      { nombre:"Veritas",       ciudad:"Los Ángeles, CA",  dias:15 },
      { nombre:"Mexotics",      ciudad:"Los Ángeles, CA",  dias:15 },
    ]
  }
};
