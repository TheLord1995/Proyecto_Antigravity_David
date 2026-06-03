# 🎬 Guión de Vídeo — Defensa Académica Antigravity

> **Proyecto:** Antigravity — Plataforma de Investigación Algorítmica con IA Supervisada
> **Fase:** 4.4 Completada · 117 Tests Passing
> **Duración estimada:** 8–10 minutos
> **Audiencia:** Tribunal académico de evaluación

---

## 🎞️ DIAPOSITIVA 1 · PORTADA

**[PANTALLA: Infografía `antigravity_infografia-V1.html` — sección cabecera]**

> *"Bienvenidos a la defensa del Proyecto Antigravity. Mi nombre es David y este es el resultado de meses de trabajo construyendo una plataforma de investigación algorítmica con IA supervisada."*

**Puntos clave a destacar:**
- Nombre del proyecto y autor
- Fase actual: **4.4 — AI Validator Contracts**
- Stack tecnológico visible: Python · FastAPI · SQLite · Monte Carlo
- Estado de seguridad: `ALLOW_REAL_EXECUTION = False`

---

## 🎞️ DIAPOSITIVA 2 · EL PROBLEMA

**[PANTALLA: Sección "¿Qué problema resuelve?" de la infografía]**

> *"El problema central que aborda este proyecto es: ¿cómo evaluar estrategias de trading algorítmico con rigor estadístico, sin ejecutar operaciones reales y sin que la IA tome decisiones autónomas en mercados financieros?"*

**Puntos clave a destacar:**
- Riesgo real de sistemas automatizados sin supervisión
- Necesidad de un pipeline determinista y auditable
- La IA como herramienta de análisis, **no de decisión**
- Ausencia de un framework académico robusto para validar backtests con Monte Carlo

---

## 🎞️ DIAPOSITIVA 3 · QUÉ ES ANTIGRAVITY

**[PANTALLA: Sección "Plataforma de Investigación" de la infografía]**

> *"Antigravity es un ecosistema modular para validar estrategias de trading. Tiene tres pilares: un motor de riesgo determinista, un motor estadístico con Monte Carlo y un validador de IA supervisada. Los tres trabajan juntos, pero la decisión final siempre es humana."*

**Puntos clave a destacar:**
- No es un bot de trading: es un **framework de validación**
- Pipeline completamente offline y sin ejecución real
- 3 capas de seguridad independientes
- SHA-256 para trazabilidad criptográfica de informes

---

## 🎞️ DIAPOSITIVA 4 · ARQUITECTURA / INFOGRAFÍA

**[PANTALLA: Sección "Pipeline Principal" de la infografía — diagrama de flujo]**

> *"El pipeline sigue este flujo. Primero, importamos el informe HTML exportado desde MetaTrader 5. El parser valida el idioma, la estructura y calcula el hash SHA-256 del archivo. A continuación, el Metrics Engine recalcula todas las métricas financieras desde cero. Después, Monte Carlo ejecuta 1.000 simulaciones para estimar el riesgo de ruina. Con esos datos, el BacktestValidator aplica 10 reglas deterministas. Y finalmente, el RiskEngine aplica 6 reglas de seguridad operativa."*

**Puntos clave a destacar:**
- Cada módulo es independiente y testeable por separado
- Sin red, sin MT5 en vivo, sin base de datos en el pipeline de validación
- La IA actúa como capa de información (INFO), no como decisor
- El resultado final pasa a aprobación humana

---

## 🎞️ DIAPOSITIVA 5 · SEGURIDAD E INVARIANTES

**[PANTALLA: Sección "Invariantes de Seguridad" de la infografía]**

> *"Aquí está el corazón del diseño de seguridad. Tres invariantes son absolutamente inviolables en el código, no en la documentación: la IA no decide, la IA no ejecuta, y la ejecución real está bloqueada de forma permanente por el RiskEngine."*

**Puntos clave a destacar:**
- `approved_for_real = False` — forzado por validador Pydantic
- `ALLOW_REAL_EXECUTION = False` — variable de entorno bloqueada
- `R1_REAL_EXECUTION_BLOCKED` — primera regla del RiskEngine
- Los intentos de modificar estos valores lanzan una excepción controlada
- 0 operaciones reales ejecutadas en toda la vida del proyecto

---

## 🎞️ DIAPOSITIVA 6 · DASHBOARD DE VALIDACIÓN

**[PANTALLA: Dashboard `antigravity_dashboard_demo-V1.html`]**

> *"Este es el dashboard de validación. Muestra el resultado completo de una ejecución demo del pipeline. Podemos ver los KPIs principales: el veredicto OBSERVATION porque el dataset demo tiene baja confianza estadística — menos de 30 trades — y el RiskEngine bloquea la ejecución real. Las métricas de estrategia se visualizan con barras de progreso coloreadas según su nivel de riesgo."*

**Señalar en pantalla:**
- KPI: `OBSERVATION` (verde)
- KPI: `RiskEngine: BLOCKED` (rojo)
- KPI: `Operaciones reales: 0` (verde)
- Pipeline visual paso a paso
- Barras de métricas: Profit Factor, Win Rate, Sortino, Drawdown, Risk of Ruin
- Gráfico de distribución Monte Carlo (percentiles P5–P95)
- Cuadro de decisiones del sistema
- Caja de invariantes activas (rojo/advertencia)

---

## 🎞️ DIAPOSITIVA 7 · DEMO FUNCIONAL

**[PANTALLA: Terminal ejecutando `demo/run_academic_demo.py` → resultado en navegador]**

> *"Ahora vamos a ver la demo funcional en vivo. Este script Python ejecuta el pipeline completo de forma determinista: carga el informe MT5 de tests/data, lo parsea, recalcula métricas, lanza Monte Carlo con 1.000 simulaciones, valida con BacktestValidator y aplica el RiskEngine. El resultado se exporta como un archivo HTML que se abre automáticamente en el navegador."*

**Secuencia de la demo:**
```
1. Ejecutar: python demo/run_academic_demo.py
2. Mostrar salida por consola (paso a paso con timestamps)
3. El navegador abre: demo/output/academic_demo_result.html
4. Señalar: clasificación, veredicto, métricas, Monte Carlo
5. Confirmar: approved_for_real = False en todo momento
```

**Puntos clave a destacar:**
- Sin datos reales ni conexión de red
- Resultado reproducible 100% (semilla Monte Carlo fija: 42)
- HTML generado con diseño premium coherente con el dashboard

---

## 🎞️ DIAPOSITIVA 8 · TESTS Y COBERTURA

**[PANTALLA: Salida de `pytest tests/ -v` en terminal]**

> *"El proyecto cuenta con 117 tests unitarios y de integración. Todos pasan. Los tests cubren el RiskEngine, los modelos Pydantic, el BacktestValidator, el Metrics Engine, el Monte Carlo, el parser MT5 y el AI Validator con sus adaptadores."*

**Puntos clave a destacar:**
- 117 tests passing, 0 fallos
- Tests de contratos de seguridad: `approved_for_real=True` lanza excepción
- Tests de invariantes: el RiskEngine siempre bloquea en modo académico
- Cobertura de edge cases: inputs inválidos, datos vacíos, formatos incorrectos

---

## 🎞️ DIAPOSITIVA 9 · ROADMAP

**[PANTALLA: Sección "Próximos Pasos" de la infografía]**

> *"El sistema está diseñado para escalar. Los siguientes pasos naturales son: añadir el RemoteAPIValidator para enriquecer el análisis de la IA, implementar la capa de aprobación por Telegram, construir el Gatekeeper MT5 para paper trading real y finalmente integrar alertas de TradingView. Pero siempre con el mismo principio: la ejecución real requiere aprobación humana explícita."*

**Puntos clave a destacar:**
- Arquitectura modular permite añadir componentes sin modificar el núcleo
- El RiskEngine es el único árbitro final antes de cualquier ejecución
- La IA escala como capa de enriquecimiento, no de control

---

## 🎞️ DIAPOSITIVA 10 · CONCLUSIÓN

**[PANTALLA: Dashboard — KPI `Operaciones reales: 0` + badge `FASE 4.4 COMPLETADA`]**

> *"En resumen: Antigravity demuestra que es posible construir un sistema de análisis algorítmico serio, estadísticamente riguroso y completamente seguro para el entorno académico. 117 tests, un pipeline de validación completo, criptografía para la trazabilidad, Monte Carlo para el riesgo y un RiskEngine determinista que garantiza en código que ninguna operación real será ejecutada jamás. Gracias."*

**Puntos de cierre:**
- GitHub: `https://github.com/TheLord1995/Proyecto_Antigravity_David`
- Stack: Python · FastAPI · Pydantic · NumPy · BeautifulSoup · SQLite
- Fase 4.4: ✅ Completada
- Tests: 117 passing · 0 fallos
- `ALLOW_REAL_EXECUTION = False` — permanente

---

## 📋 Checklist Pre-Grabación

- [ ] Infografía abierta en pantalla completa en el navegador
- [ ] Dashboard abierto en segunda pestaña
- [ ] Terminal preparada con `.venv` activado
- [ ] Script demo listo: `python demo/run_academic_demo.py`
- [ ] `pytest tests/ -v` ejecutado y resultado visible
- [ ] Micrófono probado y captura de pantalla configurada
- [ ] Iluminación y audio comprobados

---

*Guión preparado para la defensa académica del Proyecto Antigravity · Fase 4.4 · GitHub: github.com/TheLord1995/Proyecto_Antigravity_David*
