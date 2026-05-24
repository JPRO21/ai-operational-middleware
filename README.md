# AI Operational Middleware
![AI Operational Middleware Architecture](docs/architecture-diagram.png)

> Sistema operacional AI-native para automatizar generación de contenido y operaciones de marketing en negocios pequeños.

## Author

Juan Pablo Rodríguez Salas  
LinkedIn: https://linkedin.com/in/jprodriguezs

## ¿Qué es esto?

Un middleware propio construido en Python que conecta IA generativa con operaciones de negocio reales. No es un wrapper de ChatGPT. Es infraestructura operacional con contexto persistente de marca, orquestación de runtime y observabilidad completa.

La tesis: la IA generativa convertirá el contenido en commodity. La ventaja estará en la **infraestructura** que coordina, valida y escala esa generación de forma consistente.

## Arquitectura

```
Trigger Layer (n8n / webhook / cron)
        ↓
Core Engine (Python · src/main.py)
  ├── sanitize_input()
  ├── PromptOps — brand context injection
  ├── Runtime Orchestration — DEV/PROD bifurcation
  └── Pydantic validation pipeline
        ↓
Provider Layer (src/openai_client.py)
  ├── OpenAI SDK (real API)
  ├── Claude API
  └── Mock provider (safe development)
        ↓
Persistence (PostgreSQL)
  ├── brands — configuración de marca
  ├── prompts — PromptOps versionado
  ├── ai_logs — ejecuciones + cost_usd + usage metadata
  └── feedback_events — gobernanza de outputs
        ↓
Delivery Layer (n8n · Google Drive · Notion)
```

## Lo que ya funciona (Sprint 1A — COMPLETADO)

- [x] Runtime dinámico operativo
- [x] PostgreSQL conectado (`brands`, `prompts`, `ai_logs`)
- [x] PromptOps funcional con brand context injection
- [x] Pydantic validation pipeline
- [x] DEVELOPMENT_MODE con mock provider seguro
- [x] Runtime bifurcation DEV/PROD
- [x] Provider Layer aislada (`src/openai_client.py`)
- [x] OpenAI SDK integrado
- [x] Protección contra `mock_key` en producción
- [x] `ai_logs` persistiendo ejecuciones con `cost_usd`

## En progreso (Sprint 1B)

- [ ] Llamada OpenAI real con structured JSON output
- [ ] Usage metadata y token accounting
- [ ] Delivery a Google Drive vía n8n

## Stack

| Capa | Tecnología |
|---|---|
| Core Backend | Python 3.11+ |
| Database | PostgreSQL + pgAdmin |
| Prompt Ops | PromptOps versionado + JSONB |
| AI Providers | OpenAI SDK|
| Trigger / Delivery | n8n |
| Validation | Pydantic |
| Storage de outputs | Google Drive · Notion |

## Principio de diseño clave

**Python es el cerebro. n8n es el cable.**

n8n recibe webhooks, dispara ejecuciones y mueve archivos entre servicios. No toma decisiones sobre contenido, no construye prompts, no toca PostgreSQL directamente. Toda la lógica vive en Python.

## ICP (cliente objetivo)

Negocios visuales pequeños con operaciones repetitivas de contenido:
- Ecommerce lifestyle (plantas, decoración, wellness, cafés boutique)
- Instagram-heavy retail
- Hospitality pequeño

Problema que resuelven: catálogo lento, captions inconsistentes, trabajo manual sin estructura.

## Origen

Este proyecto nació de vender contenido con Midjourney. En algún punto entendí que el cuello de botella no era el contenido — era la infraestructura operacional que lo produce. Reconstruí desde esa tesis.

---

*Spec fundacional v1.3 · Fase 2 — Live Runtime Layer · Mayo 2026*