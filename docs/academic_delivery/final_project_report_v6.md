# Informe Ejecutivo: Proyecto Antigravity

**Documento de Entrega Final - Versión 6.0 (Optimizado para Evaluación Académica)**  
**Proyecto: Laboratorio Académico de Validación Segura de Sistemas Algorítmicos Asistidos por Inteligencia Artificial**  

---

## Índice

1. [Descripción del problema: La Ejecución Emocional vs. La Regla Técnica](#1-descripción-del-problema-la-ejecución-emocional-vs-la-regla-técnica)
2. [Impacto y relevancia: Evolución hacia la Responsabilidad](#2-impacto-y-relevancia-evolución-hacia-la-responsabilidad)
3. [Solución propuesta: El Laboratorio Antigravity](#3-solución-propuesta-el-laboratorio-antigravity)
4. [Uso de IA y criterio de aplicación](#4-uso-de-ia-y-criterio-de-aplicación)
5. [Prototipo desarrollado](#5-prototipo-desarrollado)
6. [Desarrollo asistido por IA (Human-in-the-Loop)](#6-desarrollo-asistido-por-ia-human-in-the-loop)
7. [KPIs (Key Performance Indicators)](#7-kpis)
8. [Gestión de Riesgos](#8-gestión-de-riesgos)
9. [Plan de implantación](#9-plan-de-implantación)
10. [Glosario de Conceptos Clave](#10-glosario-de-conceptos-clave)
11. [Conclusiones](#11-conclusiones)

---

## 1. Descripción del problema: La Ejecución Emocional vs. La Regla Técnica

El punto de partida del Proyecto Antigravity no fue originalmente la creación de un "laboratorio de software", sino la resolución de un problema crítico de negocio detectado en la **operativa de trading multiactivo individual**. Tras analizar la operativa, se identificó que el principal obstáculo no radicaba en la falta de conocimiento técnico o estadístico, sino en la **ejecución inconsistente causada por factores emocionales**. 

Un operador humano puede contar con las mejores herramientas cuantitativas y reglas estrictas de riesgo (por ejemplo, arriesgar solo el 0.5% por operación). Sin embargo, en el momento de interactuar con el mercado, la **presión emocional**, la **necesidad de recuperar pérdidas pasadas** y los **sesgos cognitivos** derivados de ligar el éxito financiero a la autoestima terminan saboteando la disciplina. El trader tiende a operar de forma compulsiva o impulsiva, ignorando su propia metodología técnica.

En definitiva, el problema real es que la emoción anula el análisis racional, provocando que se violen las reglas paramétricas de gestión de riesgo en la ejecución.

---

## 2. Impacto y relevancia: Evolución hacia la Responsabilidad

### 2.1. Del "Gatekeeper" Operativo al Entorno de Validación

Para resolver este problema, la concepción inicial del proyecto (documentada en las primeras actividades del curso y el PRD inicial) planteaba construir un "Gatekeeper" automatizado de ejecución. Este sistema preveía conectar Telegram, flujos mediante Make/n8n y una IA que evaluara el estado emocional del trader a través de justificaciones de entrada operativas. Si la IA detectaba un estado de ánimo alterado, bloquearía la conexión directa con el entorno MetaTrader 5 (MT5).

Sin embargo, a medida que maduró el diseño de la arquitectura del software y se analizó con profundidad el papel de la Inteligencia Artificial (especialmente los LLM probabilísticos), se puso en evidencia un riesgo de diseño inaceptable: **conectar un motor probabilístico a un entorno de ejecución financiera, incluso para funciones de bloqueo, sin un entorno de validación previo, viola principios elementales de seguridad y trazabilidad**.

### 2.2. La Pivotación hacia la Seguridad Académica

Por criterios de seguridad inquebrantables, trazabilidad del dato y estricta responsabilidad académica, el equipo de desarrollo decidió **no avanzar hacia la conexión de ejecución real ni simulada automatizada en esta fase**. 

El impacto y la relevancia del proyecto viraron estratégicamente hacia la creación de un **Laboratorio Académico de Validación Segura**. Al abordar la inconsistencia humana mediante la validación matemática estricta y previa, en lugar de intentar curar la emoción en el momento de la ejecución, Antigravity sienta un precedente de gobernanza inofensiva y segura. 

El sistema entrega valor como un ecosistema educativo, permitiendo auditar operaciones con rigor científico, aislando el riesgo humano sin comprometer el capital de forma irresponsable.

---

## 3. Solución propuesta: El Laboratorio Antigravity

La solución construida es **Antigravity**, un laboratorio de validación algorítmica modular que evalúa y filtra informes de backtesting y señales técnicas estableciendo un pipeline unidireccional fuertemente tipado.

### 3.1. Arquitectura del Pipeline de Validación

El flujo de datos sigue una secuencia estricta de capas independientes que garantizan que una estrategia pase por controles criptográficos, matemáticos y lógicos antes de cualquier evaluación final:

```
[Informe de Entrada (MT5 HTML)] 
        │
        ▼
┌───────────────────────┐
│     MT5 Parser        │ ──► [Generación SHA-256] ──► Registro de Integridad en SQLite
└───────────────────────┘
        │ TradeRecord[] 
        ▼
┌───────────────────────┐
│    Metrics Engine     │ ──► Recálculo matemático determinista (Sortino, Expectancy)
└───────────────────────┘
        │ Métricas Base Verificadas
        ▼
┌───────────────────────┐
│  Monte Carlo Engine   │ ──► Remuestreo estocástico y cálculo de Risk of Ruin
└───────────────────────┘
        │ Probabilidad de Ruina e Intervalos de Confianza
        ▼
┌───────────────────────┐
│   BacktestValidator   │ ──► Clasificación Lógica (REJECTED, OBSERVATION, RESEARCH_APPROVED)
└───────────────────────┘
        │ Estado de la Estrategia
        ▼
┌───────────────────────┐
│      RiskEngine       │ ──► Filtro de reglas de riesgo inquebrantables (R1–R6)
└───────────────────────┘
        │ Veredicto de Seguridad Determinista
        ▼
┌───────────────────────┐
│    Approval Layer     │ ──► Análisis contextual de IA y Dashboard
└───────────────────────┘
        │ Consolidado Enriquecido
        ▼
[Operador Humano] ──────────► Lectura y comprensión del informe validado
```

![Figura 1. Arquitectura general de Antigravity.](antigravity_infografia.png)

### 3.2. Pilares de Diseño e Invariantes de Seguridad

1. **Seguridad por diseño (Security by Design):** La infraestructura está limitada por código mediante variables inmutables como `ALLOW_REAL_EXECUTION=False` y `approved_for_real=False`, bloqueando intrínsecamente cualquier intento de escalar la validación a un entorno no simulado.
2. **Autoridad final del RiskEngine:** Como medida contra la inestabilidad de la ejecución emocional (el problema de origen), el sistema implementa un motor de reglas `RiskEngine` cien por ciento determinista que tiene prioridad y autoridad técnica absoluta sobre cualquier análisis probabilístico.

---

## 4. Uso de IA y criterio de aplicación

El núcleo de innovación de Antigravity reside en la integración segura de la IA en un flujo operativo regulado, superando el modelo del "Gatekeeper ciego" planteado inicialmente.

### 4.1. Criterio de Uso de la Inteligencia Artificial

- **Interpretación, NO decisión:** La IA asume el rol de analista técnico y psicológico. Procesa la justificación narrativa de la señal, detecta sesgos emocionales o contradicciones y emite recomendaciones. 
- **Límites inquebrantables:** Bajo ninguna circunstancia la IA ejecuta órdenes, aprueba el paso a entorno real ni omite el filtro de reglas del `RiskEngine`. La IA aporta contexto cualitativo (ej. "el usuario denota ansiedad al escribir su justificación") que complementa la rigidez del límite cuantitativo.

### 4.2. Arquitectura de Adaptadores del Validador de IA

Para asegurar la robustez de este principio, se ha implementado la IA mediante un patrón `Adapter` desacoplado:
- **Interfaces (`AIValidatorAdapter`):** Modelos de entrada y salida rigurosos (`AIValidatorInput`, `AIValidatorResult`) que fuerzan estructuralmente el rechazo de la bandera de ejecución en real.
- **Implementación Mock local (`MockAIValidator`):** Permite el desarrollo, testing de flujos de texto y la ejecución de la infraestructura completa de manera offline, logrando la fase actual del sistema sin dependencias restrictivas a redes externas.

---

## 5. Prototipo desarrollado

El laboratorio cuenta con un prototipo funcional en entorno local, garantizando coherencia íntegra entre el diseño propuesto y el código en el repositorio.

### 5.1. Stack Tecnológico de Backend
- **FastAPI:** Motor central de orquestación y endpoints.
- **Pydantic:** Invariantes de seguridad fuertemente tipadas y validación de entidades.
- **SQLite:** Bitácora inmutable de auditoría criptográfica.

### 5.2. Componentes Implementados
1. **`MT5HtmlParser`:** Parser y hasher criptográfico.
2. **`MetricsEngine` y `MonteCarlo`:** Motor de recálculo determinista y simulaciones estadísticas probabilísticas de más de 1,000 iteraciones por defecto para evaluar el riesgo de ruina.
3. **`BacktestValidator` y `RiskEngine`:** Aplicadores lógicos del marco de reglas de validación (R1 a R6) y criterios de degradación por baja confianza de simulación.
4. **`MockAIValidator`:** Capa de simulación semántica local e independiente.

### 5.3. Interfaces
El ecosistema incorpora salidas consolidadas HTML y visualización orientada al operador para asegurar que la trazabilidad sea entendible por humanos.

![Figura 2. Dashboard HTML de validación.](dashboard_antigravity.png)

### 5.4. Demo Académica Interactiva
Como entregable funcional, se dispone de una interfaz en flujo guiado que procesa iterativamente un informe: carga, parseo, generación SHA-256, cálculo de métricas de confianza Monte Carlo, validación determinista por RiskEngine y unificación de criterios en un reporte final enriquecido mediante el AI Validator.

![Figura 3. Interfaz gráfica de demostración del pipeline.](demo_gui_antigravity.png)

### 5.5. Resultados del Proyecto

Auditoría oficial del estado de los componentes implementados en el entregable del prototipo:

| Indicador / Módulo | Estado | Resultado / Observaciones |
| :--- | :---: | :--- |
| **Tests ejecutados automatizados** | 121 | Verificación rigurosa mediante `pytest`. |
| **Tests superados** | 121 | 100% de las pruebas funcionales superadas con éxito. |
| **Tests fallidos** | 0 | Sin incidencias bloqueantes. |
| **Backend FastAPI** | ✅ Implementado | Servidor base y endpoints operativos. |
| **Base de datos SQLite** | ✅ Implementada | Persistencia de trazas algorítmicas de validación. |
| **Parser MT5 & Metrics Engine** | ✅ Implementados | Criptografía y recálculo determinista activo. |
| **Monte Carlo (Risk of Ruin)** | ✅ Implementado | Simulación de estrés habilitada. |
| **BacktestValidator & RiskEngine** | ✅ Implementados | Guardián inquebrantable de reglas operativas. |
| **AI Validator Contracts (Mock)** | ✅ Implementados | Infraestructura de IA contextual y offline lista. |
| **Dashboard y Demo** | ✅ Implementados | Consolidación visual operativa del ciclo. |
| **Ejecución y entorno Real** | 🔒 Bloqueada | `ALLOW_REAL_EXECUTION=False` mantenido como constante inviolable. |

![Figura 4. Informe HTML consolidado generado automáticamente por Antigravity.](academic_demo_result.png)

---
python demo/academic_demo_gui.py
## 6. Desarrollo asistido por IA (Human-in-the-Loop)

La construcción integral de este sistema ha respondido a una aproximación de ingeniería donde el componente humano guía a los agentes de Inteligencia Artificial para evitar su desvío probabilístico:

- **Director IA Antigravity:** Actuó como Coordinador Arquitectónico, estructurando las fases del roadmap y velando por el estricto cumplimiento de los invariantes de seguridad frente a las iteraciones técnicas.
- **ChatGPT:** Ejerció como Consultor en revisiones críticas de modelos de datos Pydantic, algoritmos estocásticos de simulación y refinamiento documental.
- **VS Code + Asistentes de Entorno Local (Cline / Agentes Integrados):** Mecanismos ejecutores que tradujeron el diseño funcional a implementaciones de código de producción puras, asegurando una cobertura masiva de tests (121) bajo la continua supervisión y aprobación del operador humano.

---

## 7. KPIs (Key Performance Indicators)

El rendimiento técnico y académico del prototipo Antigravity se mide bajo indicadores concretos:
- **Calidad y Fiabilidad del Software:** Mantenimiento de **121 pruebas superadas** de integración y unitarias de forma continua.
- **Eficiencia del Análisis:** El recálculo y simulación matemática de la seguridad de una estrategia se reduce a la ejecución instantánea del `MetricsEngine` y `MonteCarlo`.
- **Integridad Documental:** **100%** de los reportes ingeridos procesados están resguardados por una firma de integridad hash SHA-256 inmutable.

---

## 8. Gestión de Riesgos

La pivoteación a un entorno académico y el rechazo de la ejecución automatizada prematura permitieron acotar significativamente el riesgo. La matriz final es la siguiente:

| Riesgo | Impacto | Mitigación Implementada |
| :--- | :---: | :--- |
| **Conexión accidental a entorno Real** | Crítico | **Inviolabilidad en Código:** El modelo forzará un error de ejecución en tiempo de compilación/ejecución ante cualquier `approved_for_real=True`. |
| **Inferencia sesgada o alucinada de IA** | Alto | **Jerarquía Determinista:** La IA analiza texto (justificaciones del trader); pero jamás tiene poder para ignorar o sustituir al `RiskEngine` que aprueba/rechaza señales. |
| **Manipulación humana del dato de origen** | Moderado | **Auditoría Criptográfica:** Todo documento MT5 procesado requiere pasar por el `MT5HtmlParser` y validarse con firma. |

---

## 9. Plan de implantación

Con la estabilización de los componentes analíticos (Fases completadas desde 1 a 4.4), el roadmap de Antigravity prevé una apertura paulatina y controlada en base al principio de la progresividad del riesgo:

1. **RemoteAPIValidator (Fase 4.4B):** Consolidación de los adaptadores de la IA reemplazando el entorno offline con integraciones a APIs como DeepSeek o Claude a través de OpenRouter.
2. **Approval Layer (Fase 4.5):** Construcción del panel interactivo avanzado para gestionar en vivo la consolidación de señales aprobadas o rechazadas.
3. **Telegram Approval Layer & Gatekeeper MT5:** Conexión asíncrona de alertas para operador y envío hacia terminales, pero confinados y restringidos de forma inmutable a cuentas de **Paper Trading (simulación con mercado real)**. Nunca cuentas operativas de producción.

---

## 10. Glosario de Conceptos Clave

Con el objetivo de facilitar la comprensión de la infografía, el dashboard interactivo y los informes HTML generados por el proyecto a perfiles no técnicos, a continuación se detallan los principales conceptos utilizados en el ecosistema:

### 10.1. Tecnologías y Motores Básicos
- **FastAPI:** Framework moderno y ultrarrápido utilizado para construir aplicaciones web e interfaces de comunicación (APIs) con Python. Por ejemplo, es la "tubería" que permite que la interfaz visual de Antigravity envíe datos al motor de cálculo subyacente y reciba respuestas instantáneas sin demoras.
- **SQLite:** Base de datos ligera, autónoma y altamente eficiente que almacena la información de manera local en un único archivo, sin requerir la instalación de grandes servidores externos. En este proyecto, funciona como la "caja fuerte" y bitácora de auditoría inmutable donde se guarda todo el historial para que no se pierda.
- **Pydantic:** Librería de validación que se encarga de forzar que la información ingresada al software tenga exactamente el formato y tipo de dato correcto. Actúa como el vigilante de seguridad de un edificio: si alguien intenta introducir un texto donde la base de datos requiere un número, Pydantic bloquea la puerta de forma inmediata e impenetrable.
- **MT5HtmlParser:** Componente (parser) desarrollado a medida para "leer y traducir" el código desestructurado de los informes de historial en formato HTML de MetaTrader 5. Su trabajo consiste en escanear el documento web exportado por el trader, ignorar los elementos visuales irrelevantes y extraer únicamente los datos numéricos puros de cada operación en un formato estructurado y útil.

### 10.2. Componentes de Seguridad y Control Operativo
- **ALLOW_REAL_EXECUTION=False:** Candado global a nivel de configuración matriz (variable de entorno) que impide físicamente que el sistema intente conectarse con servidores o envíe operaciones en vivo. Es la garantía técnica absoluta de que el software funciona y funcionará única y exclusivamente como un laboratorio académico, no como un autómata financiero real.
- **approved_for_real=False:** Campo estático e inmutable anclado en cada objeto de estrategia que impide que cualquier revisión semántica autorice una orden. Es fundamental, ya que garantiza que, incluso si la Inteligencia Artificial alucina y recomienda enérgicamente enviar una operación a mercado, la orden quedará suprimida y el mandato permanecerá inquebrantable.
- **REAL EXECUTION BLOCKED:** Veredicto contundente y estado final que devuelve la plataforma visual cuando el motor ha detenido exitosamente cualquier intento de interacción con el mercado financiero. Refleja la intervención exitosa de la capa de seguridad.
- **SHA-256:** Algoritmo matemático que procesa un archivo (como un historial de trading) y devuelve una cadena de caracteres única, actuando como una "huella dactilar" digital e inmodificable. Si un usuario manipula o maquilla tan solo una coma del informe original para aparentar mejores resultados, la firma SHA-256 cambiará drásticamente y revelará el fraude.
- **Pipeline:** Es la línea de ensamblaje o flujo de trabajo automatizado, unidireccional y riguroso por donde transita la información en el ecosistema. Su importancia reside en que obliga a cualquier informe a pasar metódicamente por las etapas de lectura, recálculo, estrés matemático e inspección cualitativa, sin que el usuario pueda saltarse ningún filtro.
- **Human-in-the-Loop:** Enfoque o filosofía de diseño de software donde el humano siempre retiene el poder de supervisión y la autoridad de la decisión final sobre la automatización. Significa que, aunque la tecnología procese miles de datos en milisegundos e IA interprete el estado emocional, es el operador quien revisa el informe y acepta formalmente el diagnóstico antes de proceder.

### 10.3. Validadores y Arquitectura Lógica
- **MetricsEngine:** Motor aritmético determinista propio de la aplicación, dedicado exclusivamente a recalcular paso por paso todas las fórmulas de un informe a partir de los datos crudos. Sirve para no confiar ciegamente en el resumen de resultados que aporta el trader, actuando como un contador independiente que verifica que no faltan fondos.
- **BacktestValidator:** Evaluador lógico que recibe los números calculados y compara su valor frente a unos umbrales o límites mínimos predefinidos para decidir la viabilidad técnica de una estrategia. Por ejemplo, si el umbral exige ganar el doble de lo que se pierde, este módulo descarta instantáneamente los sistemas que no logran esa meta.
- **RiskEngine:** Guardián superior y autoridad máxima del flujo de Antigravity; un sistema estricto basado en reglas innegociables ("Si esto ocurre, entonces detente"). A diferencia de los motores estadísticos o semánticos, este componente puede vetar de forma fulminante la operativa si detecta que se superan límites vitales como el riesgo diario de pérdida.
- **AI Validator:** Capa de integración de Inteligencia Artificial que desempeña el papel de analista de contexto y corrector psicológico sobre los comentarios escritos del trader. Su labor no es matemática, sino leer la justificación de entrada a una operación, detectar contradicciones técnicas (por ejemplo, justificar ventas usando patrones alcistas) o alertar sobre ansiedad y euforia.
- **MockAIValidator:** Versión simulada y local del AI Validator que permite probar el funcionamiento lógico de la plataforma sin tener que conectarse a internet o abonar costes de uso por API. Permite al desarrollador confirmar que la estructura del sistema reacciona correctamente a diferentes escenarios de respuesta sin depender de los servidores de OpenAI o Anthropic.
- **RemoteAPIValidator:** Módulo conectivo (planificado para fases futuras) encargado de enlazar la infraestructura interna segura con grandes y poderosos modelos lingüísticos en la nube (ej. Claude 3, DeepSeek). Será el puente definitivo que enviará el texto del trader para que una supercomputadora determine de manera sofisticada la viabilidad del contexto.

### 10.4. Conceptos Financieros y Estadísticos del Análisis
- **Monte Carlo:** Método de simulación probabilística que desordena e intercambia aleatoriamente miles de veces el orden histórico de un conjunto de operaciones. Su propósito es someter a estrés las rachas perdedoras para revelar si una estrategia es robusta en escenarios adversos, respondiendo a la pregunta: "¿Qué pasaría si mi mala suerte durara un mes?".
- **Risk of Ruin (Riesgo de Ruina):** Estimación estadística, producto de la simulación de Monte Carlo, que representa la probabilidad porcentual de que la cuenta de inversión quiebre por debajo de un punto de no retorno. Un riesgo del 30% indica que existe una alta probabilidad matemática de destruir el capital disponible, por muy buen rendimiento actual que presente la estrategia.
- **Profit Factor (Factor de Beneficio):** Métrica fundamental que indica la relación pura entre los beneficios brutos totales y las pérdidas brutas totales. Si la métrica marca un valor de 2.0, el modelo gana 2 euros por cada euro que pierde, demostrando si un algoritmo tiene realmente el viento a favor.
- **Win Rate (Porcentaje de Acierto):** Métrica porcentual que mide qué proporción de operaciones realizadas cierran con beneficios frente al total de operaciones. Si de 10 decisiones de inversión tomadas, 6 son positivas y 4 son negativas, la estrategia tiene un sólido Win Rate del 60%.
- **Drawdown:** Medida del "retroceso" o bache económico sufrido, indicando la caída en porcentaje o dinero desde el pico máximo alcanzado en el capital hasta su punto más bajo, antes de lograr una recuperación. Por ejemplo, una caída del 20% ayuda al usuario a comprender y dimensionar el sufrimiento emocional que atravesará si decide seguir operando esa estrategia.
- **Sortino Ratio:** Evolución refinada de la tradicional métrica Sharpe, cuya ventaja principal es penalizar matemática y exclusivamente la volatilidad negativa o perjudicial. Sirve para clarificar si un sistema genera riqueza asumiendo riesgos desproporcionados, premiando estrategias de crecimientos más lentos pero seguros y consistentes frente a oscilaciones a la baja.
- **Expectancy (Expectancia):** Promedio de beneficio monetario que se espera recibir en cada operación estadística futura. Si una cuenta tiene una expectancia de 10 dólares, significa que cada vez que el sistema entra al mercado (gane o pierda esa ocasión en concreto), el algoritmo deposita matemáticamente un promedio de 10 dólares netos al bolsillo a largo plazo.

### 10.5. Estados de Clasificación del Sistema
- **RESEARCH_APPROVED:** Distintivo de "Pase Verde Cuantitativo" otorgado por el sistema a estrategias y algoritmos que han superado con éxito absoluto cada fase matemática, demostrando viabilidad estructural. Queda a la espera de la Approval Layer para autorizar su paso a un entorno de prueba en tiempo real con dinero falso (Paper Trading).
- **OBSERVATION:** Etiqueta preventiva ("Semáforo Amarillo") asignada a estrategias que logran ser rentables matemáticamente, pero exhiben claras inestabilidades probabilísticas durante la prueba de estrés Monte Carlo. Advierte al operador de que el algoritmo funcionó en el pasado, pero tiene alta probabilidad de flaquear bajo variaciones del mercado.
- **REJECTED:** Decisión final inamovible de descarte y expulsión atribuida a sistemas o informes que violan los límites permitidos, suspenden expectativas, quiebran de forma catastrófica en las simulaciones o presentan firmas criptográficas manipuladas.

---

## 11. Conclusiones

El **Proyecto Antigravity** nació para solucionar la vulnerabilidad más crítica del operador humano: la ejecución emocional impulsiva y errática de los sistemas algorítmicos. La evolución técnica de la iniciativa demostró que intentar "automatizar" ciegamente ese control mediante IA incorporaba riesgos inasumibles de imprevisibilidad probabilística al mercado. 

Por tanto, Antigravity se consolidó como una infraestructura de **gobernanza, auditoría y control pre-ejecución**. 

A través de un riguroso laboratorio académico que aisla la IA, la convierte en un asesor contextual inofensivo, y entrega la autoridad de decisión final a capas deterministas blindadas (Risk Engine, Monte Carlo y Metrics recalculado), el prototipo demuestra que se puede erradicar el error de decisión emocional del trader, aportando fiabilidad académica demostrable y control riguroso de riesgos de implementación, sin comprometer un solo céntimo de capital.

---
*Documento preparado y formateado para su presentación académica final ante el tribunal del curso.*  
*approved_for_real = False | ALLOW_REAL_EXECUTION = False*  
*Copyright © 2026. Todos los derechos reservados.*
