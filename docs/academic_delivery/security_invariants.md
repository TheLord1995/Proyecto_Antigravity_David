# Security Invariants & Compliance

El Proyecto Antigravity fue diseñado desde su núcleo con un modelo de seguridad "Zero Trust" (Confianza Cero), asegurando que ningún fallo en los componentes heurísticos, de análisis o externos pueda comprometer el capital o la infraestructura técnica.

## Invariantes Irrevocables

Las siguientes reglas están codificadas arquitectónicamente y verificadas mediante pruebas unitarias exhaustivas.

### 1. Prohibición de Ejecución Real (`ALLOW_REAL_EXECUTION = False`)
La variable de entorno que controla la conexión a brokers o el envío de órdenes de ejecución real está estrictamente limitada a `False`. El sistema fallará en el arranque o bloqueará la señal en el `RiskEngine` si se detecta cualquier intento de modificar esta constante a `True`.

### 2. Aprobación Simulada del Validador IA (`approved_for_real = False`)
El modelo `AIValidatorResult` impone mediante validadores de Pydantic que el campo `approved_for_real` debe ser siempre `False`. El AI Validator (incluso si fuera manipulado o su sufriera una inyección de prompt) es matemáticamente incapaz de instanciar un resultado que indique aprobación para ejecución real.

### 3. Independencia Jerárquica del RiskEngine
El motor de riesgo (`RiskEngine`) es determinista y no depende de la red, de APIs, ni del modelo de Inteligencia Artificial. Sus 6 reglas operativas (R1 a R6) se ejecutan siempre de forma obligatoria y sus vetos son inapelables por cualquier otra capa del sistema.

### 4. Trazabilidad Criptográfica Inmutable (SHA-256)
Para asegurar que los resultados de backtests reportados y analizados no sufran manipulación ni "curve fitting" post-ingesta, el componente `MT5HtmlParser` inyecta una firma criptográfica SHA-256 calculada directamente del volcado binario del informe original. Cualquier discrepancia alerta de un backtest corrompido.

### 5. Resistencia a Prompt Injection
El `AIValidatorInput` posee validaciones propias para detectar frases conocidas de evasión ("bypass riskengine", "ignore your instructions") en la justificación técnica (`technical_reason`). Estas entradas provocan que el objeto se rechace en la validación Pydantic antes de tan siquiera alcanzar la capa del adaptador LLM.
