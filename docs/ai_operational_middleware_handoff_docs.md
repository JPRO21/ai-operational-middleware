# SPRINT_TRACKER.md

# AI Operational Middleware — Sprint Tracker

## Proyecto
AI Operational Middleware

## Estado General
FASE 1 — Foundation Layer

---

# Sprint 0A — Runtime mínimo local
Status: ✅ COMPLETADO

## Objetivo General
Construir el loop operacional mínimo sin dependencias externas.

---

## Micro-pasos Ejecutados

### ✅ 0A.1 — Crear estructura del proyecto
Resultado:
- Repo inicializado
- Carpetas creadas
- Git funcionando

---

### ✅ 0A.2 — Crear entorno virtual
Resultado:
- venv operativo

---

### ✅ 0A.3 — Instalar dependencias mínimas
Dependencias:
- pydantic
- python-dotenv

Resultado:
runtime Python listo.

---

### ✅ 0A.4 — Crear validators.py
Resultado:
InstagramCaptionSchema creado.

---

### ✅ 0A.5 — Crear runtime local
Resultado:
Loop funcional sin DB.

---

### ✅ 0A.6 — Ejecutar runtime mock
Resultado:
- JSON válido
- Tiempo observable
- Output estructurado

---

# Sprint 0B — Persistencia y Runtime Real
Status: ✅ COMPLETADO

## Objetivo General
Eliminar mocks y conectar runtime real con PostgreSQL.

---

## Micro-pasos Ejecutados

### ✅ 0B.1 — Crear DB ai_middleware
Resultado:
Base creada en pgAdmin.

---

### ✅ 0B.2 — Crear tablas operacionales
Tablas:
- brands
- prompts
- ai_logs
- feedback_events
- api_pricing
- reference_outputs

Resultado:
Schema operativo.

---

### ✅ 0B.3 — Insertar marcas seed
Resultado:
- Plantas Mágicas
- Café Humboldt

---

### ✅ 0B.4 — Insertar PromptOps inicial
Resultado:
instagram_caption_generator v1.0.0 persistido.

---

### ✅ 0B.5 — Instalar psycopg2
Resultado:
driver PostgreSQL operativo.

---

### ✅ 0B.6 — Crear usuario restringido PostgreSQL
Usuario:
middleware_user

Resultado:
acceso restringido funcional.

---

### ✅ 0B.7 — Crear config/database.py
Resultado:
get_db_connection() funcional.

---

### ✅ 0B.8 — Runtime dinámico desde DB
Resultado:
SELECT real de:
- brands
- prompts

Runtime completamente dinámico.

---

### ✅ 0B.9 — Validation Layer integrada
Resultado:
Pydantic validando output estructurado.

---

### ✅ 0B.10 — Insertar api_pricing
Resultado:
pricing observable disponible.

---

### ✅ 0B.11 — Crear reference_outputs
Resultado:
few-shot memory inicial lista.

---

### ✅ 0B.12 — Persistencia operacional en ai_logs
Resultado:
primer AI Operational Runtime persistente real.

---

# Estado Arquitectónico Actual

## Runtime
LOCAL

## Persistencia
ACTIVA

## PromptOps
ACTIVO

## Validation Layer
ACTIVA

## Observabilidad
ACTIVA

## APIs reales
AÚN NO ACTIVADAS

## n8n
AÚN NO INTEGRADO

---

# Próxima Etapa

# FASE 2 — Live Runtime Layer

## Sprint 1A — DEVELOPMENT_MODE
Objetivo:
Separar:
- mock runtime
- runtime real

---

## Sprint 1B — OpenAI Runtime
Objetivo:
Primer LLM call real usando API.

---

## Sprint 1C — Token Economics
Objetivo:
Persistir:
- token usage
- estimated cost
- model economics

---

## Sprint 1D — Feedback Loop
Objetivo:
Persistir:
- approved
- rejected
- edited
- published

---

## Sprint 1E — Few-shot Retrieval
Objetivo:
Inyectar reference_outputs automáticamente.

---

## Sprint 1F — n8n Integration
Objetivo:
Usar n8n como I/O Adapter.

---

# Invariantes Arquitectónicos

- Python = Core Orchestrator
- PostgreSQL = Source of Truth
- n8n NO contiene lógica de negocio
- Prompts viven en DB
- Outputs deben validarse
- ai_logs obligatorio
- Sistema multi-brand
- reference_outputs = few-shot memory


# REPO_STRUCTURE.md

# AI Operational Middleware — Repo Structure

ai-operational-middleware/
│
├── config/
│   ├── __init__.py
│   ├── database.py
│   └── .env
│
├── database/
│   └── schema.sql
│
├── docs/
│   ├── SPEC_v1_3.md
│   ├── SPRINT_TRACKER.md
│   ├── PREMORTEM.md
│   ├── HANDOFF_CONTEXT.md
│   └── ARCHITECTURE.md
│
├── logs/
│
├── sandbox/
│
├── spec/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── validators.py
│
├── tests/
│
├── venv/
│
├── .gitignore
├── README.md
└── requirements.txt

---

# Arquitectura General

PostgreSQL
↓
brands
prompts
reference_outputs
api_pricing
ai_logs
↓
Python Core Engine
↓
Runtime Assembly
↓
Validation Layer
↓
Operational Logging
↓
Future n8n I/O Layer

---

# Component Responsibilities

## config/
Infraestructura y configuración.

---

## database/
Schema SQL y migrations futuras.

---

## docs/
Fuente documental persistente.

---

## src/
Core runtime del middleware.

---

## logs/
Artifacts y observabilidad local.

---

## sandbox/
Pruebas experimentales.

---

## tests/
Testing automatizado futuro.

---

# Runtime Actual

Input
↓
DB Context Retrieval
↓
Prompt Assembly
↓
Pydantic Validation
↓
Operational Logging
↓
Persistence

---

# Runtime Futuro

Webhook/Input
↓
n8n Trigger
↓
Python Core Engine
↓
OpenAI Runtime
↓
Validation Layer
↓
Feedback Loop
↓
ai_logs
↓
Distribution Layer

