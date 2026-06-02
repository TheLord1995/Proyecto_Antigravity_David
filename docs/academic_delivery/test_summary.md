# Test Summary & Quality Assurance

El proyecto mantiene un enfoque en "Test-Driven Development" (TDD) y validación continua para asegurar la integridad de su núcleo financiero.

## Resumen de Ejecución
- **Framework:** `pytest`
- **Total Tests Ejecutados:** 117
- **Fallas / Errores:** 0
- **Tasa de Éxito:** 100%
- **Tiempo de Ejecución Global:** ~1.01 segundos (en entorno virtual local).

## Cobertura por Subsistema

### 1. RiskEngine (`test_risk_engine.py`)
- **Descripción:** Valida la evaluación determinista de las reglas de seguridad.
- **Pruebas Clave:** Bloqueo en ejecución real (`R1`), bloqueo si falta aprobación manual (`R2`), superación de pérdida diaria (`R3`), excedente de operaciones abiertas (`R4`), validación de UUIDs y campos requeridos (`R5`, `R6`).

### 2. Modelos de Estrategia (`test_strategy_models.py`)
- **Descripción:** Garantiza el tipado estricto de las estrategias.
- **Pruebas Clave:** Conversiones automáticas de variables, validación de checklists de clasificación y preservación de restricciones inmutables (ej. `approved_for_real = False`).

### 3. Evaluador de Backtests (`test_backtest_validator.py`)
- **Descripción:** Prueba las condiciones lógicas de promoción de una estrategia.
- **Pruebas Clave:** Rechazo por Drawdown excesivo, bajo factor de recuperación, expectativa negativa, e integridad frente a falsificaciones directas del estado.

### 4. Motor de Métricas (`test_metrics_engine.py`)
- **Descripción:** Validaciones del recálculo matemático de rendimiento.
- **Pruebas Clave:** Tolerancia a pocos trades, cálculo del impacto de comisiones en la Expectativa matemática, agrupamiento correcto de rachas y validación extrema del ratio Sortino para evitar divisiones por cero.

### 5. Monte Carlo (`test_monte_carlo.py`)
- **Descripción:** Asegura que los procesos estocásticos sean predecibles.
- **Pruebas Clave:** Reproductibilidad garantizada mediante "seeds", validación de percentiles, activación del flag `low_confidence` y rechazo matemático de matrices frágiles.

### 6. MT5 HTML Parser (`test_mt5_html_parser.py`)
- **Descripción:** Comprobación de robustez de la ingesta de datos.
- **Pruebas Clave:** Rechazo de reportes que no están en inglés, resistencia ante el parseo de HTML con DOM alterado y extracción fiel de 15 métricas distintas (Profit, Drawdown, Trades). Generación del hash criptográfico.

### 7. AI Validator Contracts (`test_ai_models.py` / `test_ai_validator_adapters.py`)
- **Descripción:** Validaciones de contratos para interacción con IA.
- **Pruebas Clave:** Restricción a valores predefinidos en ENUMs (sin comandos de ejecución de mercado), detección y fallo automático ante intentos de inyección maliciosa en texto ("bypass risk engine"), y confirmación de que la simulación offline funciona bloqueando o delegando flujos como corresponde.
