// ═══════════════════════════════════════════════════════════════
//  AGROVIP S.A. — DATOS DE MERCADO
//  Actualizado automáticamente cada jueves por GitHub Actions
//  Última actualización: 2 Jul 2026
//  ⚠ No editar manualmente — se sobreescribe cada jueves
// ═══════════════════════════════════════════════════════════════

const DATOS = {

  semana: {
    numero:      27,
    periodo:     "29–5 Jul 2026",
    actualizado: "2 Jul 2026",

    precio_productor:     0.0,
    precio_productor_ant: 0.95,

    walmart: 4.97,

    usda_ny:  36.0,
    usda_la:  17.5,
    usda_fob: 26.0,

    retail: {
      "walmart": {
            "precio_unidad": 4.97,
            "kg_equiv": 12.4,
            "url": "https://www.walmart.com/ip/Fresh-Dragon-Fruit-Each/638705858"
      },
      "publix": {
            "precio_unidad": 5.53,
            "kg_equiv": 13.8,
            "oferta": 4.41,
            "oferta_pct": 20,
            "url": "https://www.publix.com/pd/dragon-fruit/RIO-PCI-107583"
      },
      "sprouts": {
            "precio_unidad": 4.99,
            "kg_equiv": 12.5,
            "url": "https://shop.sprouts.com/store/sprouts/products/16346073-dragonfruit-pitaya-each"
      },
      "whole_foods": {
            "precio_unidad": 5.49,
            "kg_equiv": 13.7,
            "url": "https://www.wholefoodsmarket.com/product/produce-dragon-fruit-b07fzct282"
      },
      "whole_foods_lb": {
            "precio_lb": 6.99,
            "kg_equiv": 15.4,
            "nota": "Orgánico por peso",
            "url": "https://www.wholefoodsmarket.com/product/produce-dragon-fruit-b07fzct282"
      },
      "kroger": {
            "precio_unidad": 4.97,
            "kg_equiv": 12.4,
            "url": "https://www.kroger.com/p/white-dragon-fruit/0000000003040"
      }
},

    tendencia:      "incierta",
    oferta_ecuador: "baja",

    mango: true,
    fresas: false,
    blueberries: true,
    cerezas: false,
    lichi: true,
    uvas: true,

    nota: "Esta semana hay 4 competidores activos en percha: Mango México, Blueberries, Lichi, Uvas California. La pitahaya compite por espacio limitado en la sección de produce de los supermercados.",

    proyeccion: [
      { sem: 28, periodo: "Sem 28", prod: 0.85, usda_la: 16.5, dir: "alza", razon: "Menor competencia estacional." },
      { sem: 29, periodo: "Sem 29", prod: 0.81, usda_la: 16.2, dir: "baja", razon: "Presión estacional continúa." }
    ]
  },

  historial: [
    { sem:27, periodo:"29–5 Jul 2026", prod:0.0, ny:36.0, la:17.5, tend:"incierta", comps:["mango", "blueberries", "lichi", "uvas"], retail_avg:13.1 }
  ],

  config: {
    flete_mar:   1.74,
    flete_cam:   0.50,
    flete_sf:    0.65,
    margen:      0.14,
    kg_cont:     17280,
    peso_unidad: 0.40,
    margenes_cadena: {
      exportador:   0.65,
      importador:   0.22,
      distribuidor: 0.19,
      supermercado: 0.34
    }
  }
};
