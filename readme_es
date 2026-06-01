# AI Operational Middleware

![AI Operational Middleware Architecture](docs/architecture-diagram.png)

> Infraestructura operacional para workflows de generación de contenido impulsados por IA.

## Autor

Juan Pablo Rodríguez Salas

LinkedIn: https://www.linkedin.com/in/juanpablorodriguezs/

GitHub: https://github.com/JPRO21

---

# Descripción General

AI Operational Middleware es un sistema de orquestación construido en Python diseñado para transformar outputs generados por modelos de lenguaje en workflows operacionales controlados, observables y reutilizables.

No es un wrapper de ChatGPT.

El proyecto incorpora capas de operación alrededor de la generación con IA, incluyendo:

* Orquestación de runtime
* Inyección de contexto de marca
* Validación estructurada
* Monitoreo de costos
* Inteligencia operacional
* Observabilidad y trazabilidad

La tesis detrás del proyecto es simple:

> La IA generativa convertirá el contenido en commodity. La ventaja competitiva estará en la infraestructura que coordina, valida y opera esa generación de forma confiable.

---

# Arquitectura

```text
Trigger Layer
(n8n / Webhooks / Cron)
        ↓

Runtime Interface Layer
(FastAPI / Streamlit)
        ↓

Runtime Pipeline
(runtime_pipeline.py)

  ├── Sanitización de Inputs
  ├── Ensamblado de Prompts
  ├── Control de Presupuesto
  ├── Ejecución del Provider
  ├── Validación Estructurada
  ├── Runtime Intelligence
  └── Persistencia

        ↓

Provider Layer

  ├── OpenAI API
  ├── Mock Provider
  └── Futuros Providers

        ↓

Runtime Intelligence Layer

  ├── Protección de Marca
  ├── Validación Semántica
  ├── Control de Calidad
  └── Confidence Scoring

        ↓

Persistence Layer

  ├── brands
  ├── prompts
  ├── ai_logs
  ├── api_pricing
  └── feedback_events
```

---

# Estado del Proyecto

## Versión Actual

✅ Versión 1.0 — Runtime as a Service (MVP)

El middleware evolucionó desde un runtime básico para IA hasta convertirse en una plataforma operacional reutilizable capaz de servir múltiples interfaces y workflows.

---

# Funcionalidades

## Runtime Orchestration

* Pipeline reutilizable de ejecución
* Stages operacionales explícitos
* Abstracción de proveedores
* Configuración dinámica del runtime

## PromptOps

* Inyección de contexto específico por marca
* Prompts versionados
* Ensamblado estructurado de prompts

## Seguridad y Gobernanza

* Sanitización de inputs
* Protección contra prompt injection
* Control de presupuesto
* Detección de outputs inválidos
* Validaciones de seguridad

## Runtime Intelligence

* Protección de marca
* Semantic Sanity Checks
* Validación de calidad de outputs
* Generación de Confidence Score

## Interfaces

* API REST mediante FastAPI
* Documentación OpenAPI / Swagger
* Dashboard operacional en Streamlit

## Observabilidad

* Persistencia en PostgreSQL
* Registro de uso de tokens
* Monitoreo de costos
* Logs de ejecución
* Metadatos operacionales

---

# Stack Tecnológico

| Capa           | Tecnología         |
| -------------- | ------------------ |
| Backend        | Python             |
| API            | FastAPI            |
| UI             | Streamlit          |
| Validación     | Pydantic           |
| Base de Datos  | PostgreSQL         |
| Proveedor IA   | OpenAI API         |
| Automatización | n8n                |
| Observabilidad | PostgreSQL Logging |

---

# Flujo de Ejecución

```text
Datos del Producto
        ↓
Prompt Assembly
        ↓
OpenAI Runtime
        ↓
Validación Pydantic
        ↓
Runtime Intelligence
        ↓
Confidence Score
        ↓
Persistencia PostgreSQL
        ↓
Delivery Layer
```

---

# Ejemplo de Input

```json
{
  "brand_id": 1,
  "name": "Monstera Deliciosa",
  "details": "Planta tropical de interior"
}
```

# Ejemplo de Output

```json
{
  "caption": "Transforma tus espacios con la belleza tropical de una Monstera Deliciosa...",
  "hashtags": [
    "#urbanjungle",
    "#plantlover",
    "#indoorplants"
  ],
  "cta": "Visita el enlace en nuestra biografía.",
  "platform": "instagram",
  "confidence_score": 92
}
```

---

# Capacidades Demostradas

El MVP actual demuestra:

* Orquestación de workflows impulsados por IA
* Diseño de pipelines reutilizables
* Exposición de capacidades mediante APIs REST
* Validación estructurada de outputs
* Monitoreo operacional y observabilidad
* Persistencia y trazabilidad de ejecuciones
* Control de costos asociados al uso de LLMs
* Runtime Intelligence para validación y control de calidad

---

# Principio de Diseño

## Python es el cerebro. Los workflows son la capa de transporte.

Toda la lógica de negocio vive en Python.

Los sistemas externos pueden disparar ejecuciones, mover información o distribuir resultados, pero las decisiones operacionales permanecen dentro del middleware.

---

# Origen

Este proyecto nació mientras construía sistemas de generación de contenido para pequeños negocios utilizando IA generativa.

Al principio, el foco estaba en el contenido: captions, imágenes, prompts y outputs creativos. Sin embargo, después de múltiples iteraciones apareció un patrón distinto.

El cuello de botella rara vez era la generación de contenido.

Los problemas reales estaban alrededor:

* Mantener consistencia de marca
* Gestionar prompts entre distintos clientes
* Validar outputs antes de entregarlos
* Controlar costos y consumo de tokens
* Monitorear la calidad de las ejecuciones
* Construir workflows repetibles y confiables

En algún punto entendí que el cuello de botella no era el contenido.

Era la infraestructura.

La mayoría de las conversaciones sobre IA se enfocan en modelos, prompts o herramientas. Mi interés comenzó a desplazarse hacia algo diferente: cómo operar sistemas basados en IA de forma consistente, observable y controlada.

AI Operational Middleware nació como una exploración práctica de esa idea.

Más que una integración con un modelo, el proyecto busca responder una pregunta:

**¿Qué capas operacionales son necesarias para convertir una llamada a un LLM en un sistema confiable para uso real?**

El resultado fue una arquitectura centrada en orquestación, validación, observabilidad, gobernanza y control operacional.

---

# ¿Por Qué Existe Este Proyecto?

Este proyecto fue construido para explorar y demostrar conceptos relacionados con:

* AI Operations
* Workflow Automation
* Runtime Engineering
* Operational Intelligence
* Observabilidad para sistemas de IA
* Validación estructurada
* Sistemas AI-native orientados a producción

El objetivo es entender cómo operar sistemas basados en IA de forma confiable, más allá de una simple llamada a una API.

---

# Roadmap

## Versión 1.0

✅ Runtime orchestration

✅ FastAPI interface

✅ Dashboard Streamlit

✅ Runtime Intelligence

✅ Observabilidad

✅ Cost monitoring

✅ Structured validation

## Exploraciones Futuras

* Workflows de generación de imágenes
* Content Engine construido sobre este middleware
* Integraciones de entrega automatizada

---

**Versión 1.0 — Runtime as a Service MVP**

Construido por Juan Pablo Rodríguez.
