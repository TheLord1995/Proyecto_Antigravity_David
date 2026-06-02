# Pipeline Demo: Proyecto Antigravity

Este documento describe teóricamente el ciclo de vida de una señal de trading o backtest procesada por el ecosistema Antigravity, desde la ingestión hasta la resolución, demostrando la integración de los componentes de la Fase 1 a la Fase 4.4.

## Paso 1: Ingestión (MT5 HTML Import Layer)
Un operador sube un reporte de backtest de MetaTrader 5 en formato HTML (inglés) al sistema.
1. `MT5HtmlParser` lee el archivo.
2. Extrae operaciones (trades) y métricas básicas.
3. Genera un hash `SHA-256` sobre el archivo crudo para garantizar que no ha sido alterado.
4. Devuelve un objeto estructurado `BacktestReport`.

## Paso 2: Recálculo (Metrics Engine)
Para evitar confiar ciegamente en las métricas de MT5:
1. `MetricsEngine` toma la lista de operaciones extraídas.
2. Recalcula el `Expectancy`, `Profit Factor`, `Max Daily Loss` y `Sortino Ratio`.
3. Anexa estos cálculos verificados al modelo de la estrategia.

## Paso 3: Simulación Estocástica (Monte Carlo)
Se evalúa la solidez estadística de los datos históricos.
1. Se ejecutan 1,000 simulaciones de remuestreo (Bootstrap y Shuffle).
2. Se calcula la probabilidad de ruina (`Risk of Ruin`).
3. Si el percentil 95 del drawdown simulado excede el riesgo permitido, se marca `low_confidence = True`.

## Paso 4: Evaluación Lógica (BacktestValidator)
Se aplican criterios académicos y umbrales al reporte.
1. Si el Profit Factor < 1.2, se rechaza.
2. Si `low_confidence == True` (Regla D4), la estrategia máxima que puede obtener es `OBSERVATION`.
3. Si pasa todos los filtros, obtiene el estado `PAPER_TRADING_READY`.

## Paso 5: Validación Contextual de Señal (AI Validator - Fase 4.4)
*(Simulado durante esta entrega académica mediante MockAIValidator)*
Cuando la estrategia emite una señal:
1. `AIValidatorInput` consolida la dirección (BUY/SELL), precio, timeframe y justificación técnica.
2. `MockAIValidator` analiza el texto localmente (verificando contradicciones, ej. "venta" con justificación "alcista").
3. Devuelve `AIValidatorResult` recomendando revisión humana o continuación al motor de riesgo.

## Paso 6: Verificación Definitiva (RiskEngine)
Independientemente de los pasos anteriores, la señal debe pasar por el motor determinista.
1. Evalúa R1: ¿Intenta ejecutar en real? Bloqueo automático.
2. Evalúa R3 y R4: ¿Excede la pérdida diaria o número máximo de trades? Bloqueo.
3. Resultado final: `RiskResult` con estado de aprobación para entorno demo o rechazo total.

---
*Nota: Este pipeline está implementado a nivel de lógica de negocio y tests unitarios. La orquestación completa vía web (Approval Layer) forma parte de fases posteriores (4.5).*
