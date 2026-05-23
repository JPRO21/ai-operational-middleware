# AI Operational Middleware — Foundational SPEC v1.2
## Patch de Correcciones sobre v1.1 Hardened

> **Alcance de este documento:** Este no es un rediseño. Son 4 correcciones quirúrgicas
> identificadas por pre-mortem sobre el v1.1. Todo lo demás del v1.1 permanece vigente
> sin cambios. Leer este documento junto con el v1.1, no en reemplazo.

---

## Corrección 1 — Resolución de la Contradicción n8n
**Afecta:** Sección 8 (Stack Tecnológico) y Sección 9 (Core Principle) del v1.1  
**Tipo de falla:** Contradicción estructural activa

### Problema
La sección 8 lista n8n bajo el título "Orchestration". La sección 9 dice que n8n
"solo dispara, conecta, distribuye". Estos dos roles son contradictorios. "Orchestration"
implica coordinación de lógica; "dispara y distribuye" implica transporte pasivo.
Un developer que lee la sección 8 tiene justificación para poner lógica en n8n.
Un developer que lee la sección 9 no. Esta ambigüedad se va a resolver de forma
incorrecta bajo presión de tiempo.

### Resolución
n8n **no es Orchestration** en este sistema.

El rol oficial de n8n es: **Delivery & Trigger Layer**.

Definición operacional:

- n8n **puede**: recibir webhooks, ejecutar scripts Python como subprocesos,
  mover archivos, enviar notificaciones, publicar en APIs externas (Drive, Notion,
  Instagram drafts).
- n8n **no puede**: tomar decisiones condicionales sobre contenido, contener
  validaciones de negocio, modificar o construir prompts, leer o escribir
  en las tablas `brands`, `prompts`, o `feedback_events` directamente.

La sección 8 del v1.1 debe leerse con n8n bajo el título **"Delivery Layer"**,
no "Orchestration". Toda referencia futura a n8n como orquestador queda
oficialmente descartada.

---

## Corrección 2 — Control de Costos con Precios Versionados
**Afecta:** Protocolo 3 (Control de Costos) del v1.1  
**Tipo de falla:** Regla de negocio sin enforcement técnico

### Problema
El Protocolo 3 dice que el Core Engine calculará el costo "multiplicando por el
valor vigente del modelo". No define dónde vive ese valor. Si está hardcodeado
en el código Python, se desactualiza silenciosamente cuando OpenAI o Anthropic
cambian precios o deprecan modelos. El margen mínimo del 70% se convierte en
una aspiración en lugar de una restricción ejecutable.

### Resolución

#### Nueva tabla: `api_pricing`

```sql
CREATE TABLE api_pricing (
    id              SERIAL PRIMARY KEY,
    model_name      VARCHAR(100) NOT NULL,
    input_price_per_1k  NUMERIC(10, 6) NOT NULL,
    output_price_per_1k NUMERIC(10, 6) NOT NULL,
    effective_date  DATE NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    notes           TEXT
);

-- Índice para lookup rápido en runtime
CREATE INDEX idx_api_pricing_active ON api_pricing(model_name, is_active);
```

#### Regla operacional
El Core Engine (`src/main.py`) **nunca define precios como constantes**.
En cada llamada a la API, el costo se calcula así:

```python
# Pseudocódigo — implementar en el módulo de logging
def calculate_cost(model_name: str, input_tokens: int, output_tokens: int, db_conn) -> float:
    pricing = db_conn.fetchone(
        "SELECT input_price_per_1k, output_price_per_1k "
        "FROM api_pricing WHERE model_name = %s AND is_active = TRUE "
        "ORDER BY effective_date DESC LIMIT 1",
        (model_name,)
    )
    if not pricing:
        raise ValueError(f"No pricing found for model: {model_name}. Update api_pricing table.")
    
    cost = (input_tokens / 1000 * pricing['input_price_per_1k'] +
            output_tokens / 1000 * pricing['output_price_per_1k'])
    return cost
```

Si no existe pricing para el modelo en la tabla, el sistema lanza error en lugar
de ejecutar con costo desconocido. Esto convierte un fallo silencioso en un
fallo visible.

#### Alerta de margen en el Cuadrante de Observabilidad (Query adicional)

```sql
-- Query 5 (nueva): Alerta de degradación de margen
-- Ejecutar junto con las 4 queries semanales del v1.1
SELECT
    brand_id,
    ROUND(AVG(cost_usd), 4) AS avg_cost_this_week,
    LAG(ROUND(AVG(cost_usd), 4)) OVER (PARTITION BY brand_id ORDER BY week) AS avg_cost_prev_week,
    CASE
        WHEN AVG(cost_usd) > LAG(AVG(cost_usd)) OVER (PARTITION BY brand_id ORDER BY week) * 1.05
        THEN 'ALERTA: costo subió +5% vs semana anterior'
        ELSE 'OK'
    END AS margin_status
FROM (
    SELECT brand_id, cost_usd, DATE_TRUNC('week', created_at) AS week
    FROM ai_logs
    WHERE created_at >= NOW() - INTERVAL '14 days'
) weekly
GROUP BY brand_id, week;
```

---

## Corrección 3 — Validación de Comportamiento en Café Humboldt
**Afecta:** Protocolo 1 (Segundo Cliente Virtual) del v1.1  
**Tipo de falla:** Validación de estructura sin validación de comportamiento

### Problema
El Protocolo 1 define éxito como "el schema JSONB de brand_config puede modelar
simultáneamente las necesidades de ambos nichos sin alterar una línea de código".
Esto valida estructura (los campos existen y son válidos) pero no valida
comportamiento (los outputs generados son distinguibles y correctos para cada marca).
Un pipeline puede aceptar dos configs radicalmente distintos y producir outputs
que suenan iguales. La genericidad del código es necesaria pero no suficiente.

### Resolución

#### Criterio de validación extendido para el Protocolo 1

El Protocolo 1 se considera completo solo cuando se cumplen **ambas** condiciones:

**Condición A — Estructura (ya estaba en v1.1):**  
El schema de `brand_config` acepta configs de Plantas Mágicas y Café Humboldt
sin modificar `src/main.py`.

**Condición B — Comportamiento (nueva):**  
Con el mismo prompt activo, el pipeline produce outputs que un observador
externo puede distinguir como pertenecientes a marcas diferentes. Criterio
mínimo: 3 outputs de Plantas Mágicas y 3 outputs de Café Humboldt evaluados
lado a lado por el developer. Si los 6 outputs suenan intercambiables,
el brand_config de Café Humboldt está incompleto, no el código.

#### Outputs de referencia para Café Humboldt

Antes del fin de la semana 1, crear manualmente 5 outputs de referencia para
Café Humboldt que definan el tono correcto. Estos outputs no se generan con IA
inicialmente — se escriben a mano como "así debería sonar esto". Funcionan como
test de regresión: si el pipeline produce algo que podría pertenecer a Plantas
Mágicas, la validación falla.

Guardar estos outputs en la tabla `brands` bajo un campo `reference_outputs JSONB`
o en un archivo `tests/cafe_humboldt_reference.json`.

---

## Corrección 4 — Definición de la Firma de Consistencia
**Afecta:** Protocolo 5 (Período de Calibración) del v1.1  
**Tipo de falla:** Hito de proceso sin contenido definido

### Problema
El Protocolo 5 describe el onboarding y termina con "Firma de Consistencia" como
condición para pasar al Monthly Usage. El término aparece en el diagrama pero
nunca se define. En la práctica, es un placeholder que genera ambigüedad en el
momento más crítico de la relación con el cliente: el cierre del período de
calibración.

### Resolución

#### Definición operacional de la Firma de Consistencia

La Firma de Consistencia es un documento de una sola página que contiene:

1. **10 outputs aprobados** — ejemplos reales generados por el sistema durante
   el período de calibración, seleccionados y firmados por el `reviewer_role = 'owner'`.
2. **brand_config vigente** — el JSON completo del config activo al día 30,
   impreso o exportado como PDF adjunto.
3. **Prompts activos** — lista de los `prompt_id` activos con sus versiones
   (`version_tag`) y una línea de descripción de cada uno.
4. **Declaración de alcance** — dos párrafos definiendo qué genera el sistema
   (scope) y qué no genera (fuera de scope). Firmado por ambas partes.

#### Protocolo de extensión

Si el día 30 el cliente no puede firmar porque los outputs no son satisfactorios,
el período de calibración se extiende en bloques de 7 días adicionales. Cada
extensión se cobra a la misma tarifa diaria del fee de configuración original.
El operador no absorbe el costo de calibraciones incompletas por falta de
disponibilidad del cliente.

Este protocolo de extensión debe estar en el contrato de servicio antes de
iniciar cualquier calibración.

---

## Resumen de cambios respecto al v1.1

| # | Sección afectada | Tipo de cambio |
|---|---|---|
| C1 | Stack (n8n) | Reclasificación de rol: Orchestration → Delivery Layer |
| C2 | Protocolo 3 + ai_logs | Nueva tabla `api_pricing` + función de costo en runtime + Query 5 |
| C3 | Protocolo 1 | Extensión del criterio de validación: estructura + comportamiento |
| C4 | Protocolo 5 | Definición completa de Firma de Consistencia + protocolo de extensión |

---

## Estado del SPEC tras v1.2

Los 7 post-mortems del pre-mortem v1 están resueltos.  
Las 4 fragilidades nuevas identificadas en el pre-mortem v1.1 están resueltas.  
La contradicción estructural de n8n está resuelta.

**El SPEC puede considerarse congelado para la ejecución del plan de 30 días.**

El único supuesto que permanece como riesgo aceptado y monitoreable:
los precios de APIs externas y la estabilidad de los modelos son variables
del entorno, no del sistema. La tabla `api_pricing` convierte ese riesgo
en visible y accionable — no lo elimina.

---

*Documento generado como corrección quirúrgica sobre v1.1 Hardened.*  
*Fecha: 20 mayo 2026*
