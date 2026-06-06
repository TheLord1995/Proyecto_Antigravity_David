# Roadmap: Próximos Pasos

## 📋 Resumen del Roadmap

El proyecto Antigravity sigue una hoja de ruta modular estricta. Actualmente se ha completado hasta la **Fase 4.4 (AI Validator Contracts & Mock)**, integrando ingesta segura de reportes MT5, cálculo matemático avanzado (Metrics Engine), análisis estocástico (Monte Carlo & Risk of Ruin), y la arquitectura por adaptadores del validador de IA (con implementación Mock local). Las siguientes fases abordarán la integración remota con APIs de IA, la interfaz de aprobación humana y la conectividad controlada.

---

## 🗺️ Fases del Proyecto

```
Fase 1: Fundamentos                 ✅ COMPLETADO
Fase 2: Riesgo y Framework          ✅ COMPLETADO
Fase 3: Validación Académica        ✅ COMPLETADO
Fase 4.1: MT5 Import Layer          ✅ COMPLETADO
Fase 4.2A: Metrics Engine Base      ✅ COMPLETADO
Fase 4.2B: Monte Carlo & Risk Ruin  ✅ COMPLETADO
Fase 4.3 & 4.4: AI Contracts/Mock   ✅ COMPLETADO
────────────────────────────────────────────────────────
Fase 4.4B: RemoteAPIValidator       🔜 PRÓXIMO
Fase 4.5: Approval Layer            📅 PLANIFICADO
Fase 5.1: Telegram Approval Layer   📅 PLANIFICADO
Fase 5.2: Kill Switch               📅 PLANIFICADO
Fase 6.1: Paper Trading Sandbox     📅 PLANIFICADO
Fase 6.2: Gatekeeper MT5 & n8n      📅 PLANIFICADO
Fase 6.3: TradingView Integration   📅 PLANIFICADO
Fase 7: Demo Execution              📅 PLANIFICADO
Fase 8: Ejecución Real              🔒 BLOQUEADO
```

---

## ✅ Fase 4.2B: Monte Carlo & Risk of Ruin (COMPLETADA)

### Descripción
Evolución del Metrics Engine para calcular métricas estocásticas avanzadas que requieran simulaciones de remuestreo.

### Objetivos
- [x] Algoritmo de simulación Monte Carlo sobre la lista de transacciones.
- [x] Cálculo probabilístico de Risk of Ruin.
- [x] Integración condicional en el BacktestValidator para aplicar umbrales probabilísticos.

---

## ✅ Fase 4.3 & 4.4: AI Validator Design & Contracts (COMPLETADA)

### Descripción
Módulo de validación cualitativa que utiliza agentes IA para analizar contextos operativos antes de aprobar estrategias o transacciones.

### Objetivos
- [x] Establecer arquitectura de adaptadores desacoplada (Mock, RemoteAPI, OllamaRemote para VPS futuro).
- [x] Diseñar e implementar contratos de datos Pydantic (AIValidatorInput y AIValidatorResult).
- [x] Crear el validador offline MockAIValidator para depuración y testeo sin red.
- [x] Tests unitarios con 100% de cobertura y bloqueo estricto de approved_for_real.

---

## 🔜 Fase 4.4B: RemoteAPIValidator

### Descripción
Conexión remota del validador de IA con APIs de inteligencia artificial gestionadas en la nube (e.g. OpenRouter/Gemini/Claude).

### Objetivos
- [ ] Implementar adaptador `RemoteAPIValidator` en `core/ai_validator.py`.
- [ ] Conectar con OpenRouter, Gemini o Claude a través de llamadas HTTP seguras.
- [ ] Diseñar prompts de validación técnica de mercado (análisis fundamental, noticias y volumen).
- [ ] Registrar la latencia y la clave de modelo utilizada en el log.

---

## 📅 Fases de Seguridad y Control Operativo (Fase 5)

### Fase 5.1: Telegram Approval Layer
Capa de aprobación que requiere confirmación humana asíncrona antes de transitar a estados de ejecución simulada. Notificaciones integradas y sistema de tokens OTP o callbacks. Todo trade debe ser aprobado explícitamente.

### Fase 5.2: Kill Switch
Sistema de parada de emergencia integral (`/emergency/stop`) para bloquear instantáneamente todas las operaciones y congelar el Gatekeeper. Debe persistir el estado hasta desactivarse manualmente.

---

## 📅 Fases de Conectividad y Simulación (Fase 6)

### Fase 6.1: Paper Trading Sandbox
Entorno virtual de simulación total de mercado que consume señales validadas sin conectar al broker. Simula operaciones, calcula balance/equity virtual y genera reportes de rendimiento.

### Fase 6.2: Gatekeeper MT5 & n8n
Orquestador central. Módulo de puente seguro (`Gatekeeper`) y orquestación externa con `n8n` para enrutar intentos de operación a instancias controladas de MT5 (Demo). Maneja buffer de señales y retry logic.

### Fase 6.3: TradingView Integration
Receptor de webhooks de señales de TradingView. Autenticación con tokens y transformación de alertas genéricas a eventos operativos validados en el pipeline.

---

## 📅 Fase 7: Demo Execution

### Descripción
Conexión exclusiva con instancias de broker en entorno de simulación (Demo account de MT5). Esta será la máxima expresión operativa permitida.

---

## 🔒 Fase 8: Ejecución Real

### ⚠️ IMPORTANTE: Esta fase está BLOQUEADA PERMANENTEMENTE

La ejecución con dinero real **NUNCA** será parte de este proyecto académico por razones de seguridad y cumplimiento.

### Razones del Bloqueo
1. **Riesgo financiero**: Operaciones reales requieren licencias y regulación.
2. **Seguridad**: El proyecto es académico y educativo.
3. **Responsabilidad**: No nos hacemos responsables de pérdidas financieras.

### Pipeline Oficial (No saltable)
`Parser → Metrics Engine → BacktestValidator → RiskEngine → Approval Layer`

Cualquier ejecución operativa futura requiere obligatoriamente completar este pipeline, y la variable global `ALLOW_REAL_EXECUTION` siempre estará en `False` por diseño contractual (`approved_for_real=False`).

---

## 🎯 Prioridades de Desarrollo Actuales

| Prioridad | Fase | Descripción |
|-----------|------|-------------|
| **ALTA** | 4.2B | Monte Carlo & Risk of Ruin - Cierre analítico cuantitativo |
| **ALTA** | 4.3 | AI Validator - Verificación heurística con LLM |
| **MEDIA** | 5.1 | Telegram Approval Layer - Human-in-the-loop |
| **MEDIA** | 5.2 | Kill Switch - Sistema de bloqueo de emergencia |
| **MEDIA** | 6 | Conectividad y Simulación |
| **BAJA** | 7 | Demo Execution |
| **NULA** | 8 | Ejecución Real - ❌ BLOQUEADO |

---

## 🔧 Cómo Continuar el Desarrollo

### Setup del Entorno
```bash
# Activar entorno virtual
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests globales
pytest tests/

# Arrancar servidor
python -m uvicorn core.main:app --reload
```

---

## 📚 Referencias

- Documento de Arquitectura: `docs/architecture/ARCHITECTURE_OVERVIEW.md`
- Contexto IA: `docs/ai_context/ANTIGRAVITY_SPACE_CONTEXT.md`
- Estado del Proyecto: `docs/management/PROJECT_STATUS.md`

---

## ⚠️ Disclaimer

Este roadmap es para fines educativos y académicos. El proyecto **NO** está diseñado para uso en producción financiera real.
