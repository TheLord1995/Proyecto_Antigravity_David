# MT5 Backtest Strategy Guide

Este documento define el marco normativo y metodológico para la validación y auditoría de estrategias generadas por el sistema mediante backtesting en MetaTrader 5. **No es una recomendación de trading ni una estrategia ejecutable.**

## 1. Calidad del Modelado (Modeling Quality)
- **Requisito mínimo:** La calidad del modelado en MT5 debe ser del **99% o superior**. 
- **Modo de generación de ticks:** Se debe utilizar estrictamente el modo **"Every tick based on real ticks"** para garantizar que los backtests reflejan con máxima precisión las condiciones históricas del mercado.

## 2. Costes Reales de Operación
Todo backtest debe incorporar los siguientes costes reales del mercado:
- **Spread:** Variable (flotante) basado en el histórico real del broker.
- **Comisiones:** Reflejando la estructura de comisiones del broker.
- **Slippage (Deslizamiento):** Consideración de latencia o retrasos razonables.

## 3. Separación de Datos (In Sample / Out of Sample)
- **In Sample (IS):** Período utilizado por el modelo de IA para el entrenamiento, análisis y definición inicial de los parámetros.
- **Out of Sample (OOS):** Período *completamente ciego* utilizado exclusivamente para la validación del modelo. El rendimiento en OOS determinará la viabilidad de la estrategia.

## 4. Control de Overfitting (Sobreoptimización)
- Evitar curvas de capital hiper-perfectas sin drawdowns lógicos.
- Confirmar consistencia a lo largo de diferentes regímenes de mercado.
- La degradación de métricas entre In Sample y Out of Sample no debe exceder los umbrales de tolerancia del RiskEngine.

## 5. Especificaciones Técnicas y Operativas
- **Magic Number:** Toda estrategia debe contar con un *Magic Number único* para asegurar un tracking exacto de sus operaciones, permitiendo al sistema distinguir entre diferentes algoritmos.
- **Símbolos (Sufijos de Broker):** Se deben utilizar los símbolos específicos requeridos por la cuenta del broker (ej. `EURUSD.r`, `XAUUSD.ecn`).
- **Modos de Ejecución:**
  - *Modo Visual:* Utilizado para la depuración y comprobación de la lógica de entrada/salida.
  - *Modo Normal (Non-Visual):* Requerido para pruebas de rendimiento y validación final rápida.

## 6. Métricas de Validación Requeridas
Toda estrategia debe superar la evaluación del `BacktestValidator` incluyendo:
- **Profit Factor:** Ganancias brutas / Pérdidas brutas.
- **Drawdown:** Evaluación rigurosa de las caídas máximas permitidas.
- **Sharpe Ratio:** Medición del rendimiento ajustado al riesgo.
- **Número Mínimo de Operaciones:** Se requiere significancia estadística para validar cualquier resultado de backtesting.

---
**Restricciones Activas (No modificables por la IA):**
* `ALLOW_REAL_EXECUTION=False`
* `approved_for_real=False`
* Ninguna ejecución real está permitida sin la aprobación final y explícita del pipeline de seguridad (RiskEngine, Humano).
