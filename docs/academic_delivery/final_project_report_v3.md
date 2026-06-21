# Informe Ejecutivo: Proyecto Antigravity

**Documento de Entrega Final - Versión 3.0 (Optimizado para Evaluación Académica)**  
**Proyecto: Laboratorio Académico de Validación Segura de Sistemas Algorítmicos Asistidos por Inteligencia Artificial**  

---

## Índice

1. [Descripción del problema](#1-descripción-del-problema)
2. [Impacto y relevancia](#2-impacto-y-relevancia)
3. [Solución propuesta](#3-solución-propuesta)
4. [Uso de IA y criterio de aplicación](#4-uso-de-ia-y-criterio-de-aplicación)
5. [Prototipo desarrollado](#5-prototipo-desarrollado)
6. [Desarrollo asistido por IA (Human-in-the-Loop)](#6-desarrollo-asistido-por-ia-human-in-the-loop)
7. [KPIs (Key Performance Indicators)](#7-kpis)
8. [Gestión de Riesgos](#8-gestión-de-riesgos)
9. [Plan de implantación](#9-plan-de-implantación)
10. [Conclusiones](#10-conclusiones)

---

## 1. Descripción del problema

### 1.1. El auge de la Inteligencia Artificial en el Diseño de Algoritmos
En los últimos años, el uso de la Inteligencia Artificial (IA) y de los Modelos de Lenguaje de Gran Tamaño (LLMs) ha revolucionado la creación de sistemas algorítmicos. Tradicionalmente, codificar una estrategia requería conocimientos matemáticos y de programación avanzados. Hoy en día, las herramientas de IA generativa permiten a estudiantes, investigadores y desarrolladores generar código, lógica operativa e indicadores en cuestión de minutos. 

### 1.2. El Riesgo del Determinismo vs. Probabilidad
Sin embargo, esta facilidad de generación esconde un riesgo crítico. La IA opera bajo principios de probabilidad (análisis semántico, inferencia lingüística y extrapolación de patrones) y es susceptible a cometer alucinaciones o inducir a errores lógicos en el código. Confiar ciegamente en un sistema probabilístico para gobernar decisiones complejas—especialmente aquellas que involucran la gestión de recursos o riesgos—puede generar fallos catastróficos si no existen filtros deterministas estrictos de control.

### 1.3. La Ausencia de Marcos de Validación Rigurosos
El problema estructural actual es la falta de infraestructuras que auditen de forma independiente el rendimiento y la seguridad del software generado por IA. Los principales desafíos a resolver son:
- **Problemas de sobreajuste (overfitting):** Los algoritmos suelen estar optimizados en exceso para un único conjunto de datos del pasado. Al enfrentarse a variaciones reales, el sistema falla por su incapacidad de generalización estadística.
- **Falta de trazabilidad e integridad:** Los informes brutos de rendimiento que sirven de base para evaluar un algoritmo pueden manipularse fácilmente en formato de texto o HTML, lo que compromete la veracidad del proceso de auditoría.
- **Necesidad de gobernanza y control:** No existe una línea clara de separación entre el motor analítico probabilístico (la IA) y la regla inmutable de seguridad (el software determinista).

Por tanto, existe una necesidad imperiosa de diseñar e implementar **laboratorios académicos de validación y control** que actúen como filtros inviolables de seguridad antes de cualquier despliegue operativo en simulación.

---

## 2. Impacto y relevancia

### 2.1. Destinatarios del Ecosistema
El Proyecto Antigravity se posiciona como una infraestructura educativa y de investigación dirigida a:
- **Estudiantes e Investigadores Cuantitativos:** Ofrece un entorno seguro para someter sus tesis, modelos predictivos y algoritmos a pruebas de estrés estadístico sin riesgos financieros ni legales.
- **Desarrolladores de Software:** Proporciona un marco de trabajo (framework) modular que integra validación semántica de IA y lógica restrictiva pura de riesgo.
- **Laboratorios Académicos y Entornos de Experimentación:** Funciona como un sandbox local completo e inofensivo para la enseñanza de las finanzas cuantitativas y la ingeniería de software seguro.

### 2.2. Valor Académico y Científico Generado
El impacto del proyecto radica en la mitigación de los errores humanos y algorítmicos a través de la formalización de procesos:
1. **Reducción del error de confirmación y fallos algorítmicos:** Al recalcular matemáticamente de forma interna cada métrica y forzar simulaciones de tipo estocástico (azaroso), la plataforma desmitifica los resultados optimistas de los sistemas mal validados.
2. **Garantía de integridad de datos y mejora de la trazabilidad:** A través del uso de hashes de seguridad, el laboratorio asienta un precedente en la trazabilidad académica de proyectos.
3. **Entorno seguro para el aprendizaje de IA Responsable:** Los usuarios aprenden a diseñar sistemas híbridos donde la IA enriquece el proceso con contexto lingüístico, pero bajo ningún pretexto toma la decisión del control final del riesgo.

---

## 3. Solución propuesta

La solución es **Antigravity**, un laboratorio modular que establece un pipeline unidireccional y blindado de datos para la gobernanza de sistemas algorítmicos.

### 3.1. Arquitectura del Pipeline de Validación
El flujo de datos sigue una secuencia lógica de capas independientes que no se pueden omitir ni evitar de forma unilateral:

```
[Informe de Entrada] 
        │
        ▼
┌───────────────────────┐
│     MT5 Parser        │ ──► [Generación SHA-256] ──► Registro en SQLite
└───────────────────────┘
        │ TradeRecord[] (Integridad Asegurada)
        ▼
┌───────────────────────┐
│    Metrics Engine     │ ──► Recálculo matemático determinista
└───────────────────────┘
        │ Métricas Base (Expectancia, Sortino, etc.)
        ▼
┌───────────────────────┐
│  Monte Carlo Engine   │ ──► Pruebas de estrés y cálculo del Risk of Ruin
└───────────────────────┘
        │ Probabilidad de Ruina e Intervalos de Confianza
        ▼
┌───────────────────────┐
│   BacktestValidator   │ ──► Clasificación (REJECTED, OBSERVATION, READY)
└───────────────────────┘
        │ Estado de la Estrategia
        ▼
┌───────────────────────┐
│      RiskEngine       │ ──► Evaluación de reglas inquebrantables R1–R6
└───────────────────────┘
        │ Veredicto de Seguridad
        ▼
┌───────────────────────┐
│    Approval Layer     │ ──► Presentación visual en el Dashboard
└───────────────────────┘
        │ Consolidado
        ▼
[Operador Humano] ──────────► Decisión manual / Acción simulada
```

### 3.2. Pilares de Diseño
- **Seguridad por diseño (Security by Design):** El sistema arranca de manera predeterminada con bloqueos absolutos de ejecución en entornos no simulados. Las variables globales `ALLOW_REAL_EXECUTION=False` y `approved_for_real=False` están fuertemente inyectadas en las estructuras de datos y validadas mediante pruebas automatizadas.
- **Separación de responsabilidades:** Cada módulo tiene una función única. El Parser no calcula, el motor matemático no decide, y la IA no ejecuta. 
- **Autoridad final del RiskEngine:** Aunque el validador semántico por IA o la propia clasificación del algoritmo arrojen veredictos altamente positivos, el **RiskEngine** (un motor estrictamente lógico y determinista) tiene la potestad absoluta de bloquear de forma autónoma cualquier señal si viola una sola regla de seguridad paramétrica.

---

## 4. Uso de IA y criterio de aplicación

El núcleo de innovación de Antigravity reside en la integración segura de la IA en un flujo operativo regulado.

### 4.1. Criterio de Uso de la Inteligencia Artificial
La Inteligencia Artificial se utiliza únicamente para lo que es excelente: **interpretación contextual, análisis cualitativo y traducción semántica**.

- **¿Por qué utilizar IA?** Los motores matemáticos convencionales detectan anomalías numéricas, pero no entienden la razón subyacente. La IA actúa como un analista que lee el porqué técnico expuesto por el usuario (`technical_justification`), detecta incoherencias lógicas con respecto a los parámetros y genera una explicación legible en lenguaje natural sobre posibles debilidades que las matemáticas no perciben (por ejemplo, contradicciones en la dirección elegida en base a la descripción del mercado).
- **¿Por qué limitar la IA?** Los LLMs son probabilísticos. No se puede garantizar en un 100% que una IA no alucine en su veredicto o que no sea vulnerable a inyecciones de instrucciones externas (Prompt Injections). 

Por lo tanto, la regla de gobernanza inmutable de Antigravity establece:  
**La IA analiza, explica y aconseja, pero JAMÁS decide, JAMÁS ejecuta y JAMÁS puede saltarse el RiskEngine.**

### 4.2. Arquitectura de Adaptadores del Validador de IA
Para evitar dependencias y aislar el núcleo del sistema, se ha diseñado un patrón `Adapter/Provider`:
- **`AIValidatorAdapter`:** Interfaz abstracta que define el contrato de datos común del módulo.
- **`AIValidatorInput` y `AIValidatorResult`:** Modelos de datos de Pydantic que fuerzan un tipado estricto en la entrada y en la salida, obligando a mapear campos como el UUID de la señal, la lista de contradicciones y el indicador de control `approved_for_real=False`.
- **`MockAIValidator`:** Implementación local puramente offline. Permite el funcionamiento continuo del laboratorio sin depender de una red o API externa congestionada, evaluando de manera rápida si la justificación contiene palabras clave o contradicciones obvias.
- **`RemoteAPIValidator` (Roadmap):** Adaptador que conectará de manera asíncrona con modelos externos en la nube a través de agregadores o APIs directas.

> [!NOTE]
> La **Fase 4.4 (AI Validator Contracts)** ha sido completada con éxito. Esto significa que la arquitectura técnica del adaptador, las interfaces de tipado y el funcionamiento simulado local (Mock) están plenamente operativos y validados mediante pruebas automatizadas.

---

## 5. Prototipo desarrollado

El laboratorio cuenta con un prototipo real y completamente funcional en entorno local, estructurado sobre bases estables de ingeniería de software.

### 5.1. Stack Tecnológico de Backend
- **FastAPI:** Framework moderno de alto rendimiento para el desarrollo de la API web del laboratorio.
- **Pydantic:** Garantiza la validación rigurosa de tipos de datos en tiempo de ejecución, impidiendo entradas corruptas en el pipeline.
- **SQLite:** Base de datos relacional integrada para guardar de forma inmutable la bitácora de auditoría y los logs de validación.

### 5.2. Componentes de Software Implementados
1. **`MT5HtmlParser`:** Parser robusto que lee e interpreta de forma limpia informes de auditoría técnica externos (en inglés y español), sanitizando el HTML y generando firmas SHA-256 de control para evitar fraudes de datos.
2. **`MetricsEngine`:** Módulo aislado de recálculo determinista de Sortino Ratio, Expectancia y métricas clave sobre el vector de operaciones.
3. **`MonteCarlo`:** Motor estocástico que realiza hasta 1,000 simulaciones de remuestreo (Bootstrap y Shuffle) para verificar la supervivencia del algoritmo y el riesgo de ruina (`risk_of_ruin_pct`).
4. **`BacktestValidator`:** Evaluador lógico de políticas de aceptación de estrategias.
5. **`RiskEngine`:** El guardián determinista que aplica las 6 reglas inquebrantables de seguridad operativa a nivel de simulación.
6. **`MockAIValidator`:** El validador semántico local offline que ejecuta validaciones contextuales de texto y estructura.

### 5.3. Interfaces
- **Dashboard HTML de Validación:** Panel gráfico estático interactivo que permite visualizar de forma unificada las métricas del motor de cálculo, las trayectorias de Monte Carlo, el estado de aceptación por `BacktestValidator` y las evaluaciones de la capa de riesgo.
- **Consola Swagger interactiva:** Interfaz nativa de FastAPI (disponible en `/docs`) que permite al usuario interactuar en tiempo de ejecución con los endpoints de validación de operativas y salud del servicio.

### 5.4. Demo Académica Interactiva
Como demostración funcional del proyecto, se ha desarrollado una interfaz interactiva de flujo guiado que permite visualizar todo el pipeline completo de la infraestructura. Esta demo realiza los siguientes pasos:
1. **Selección de informe MT5:** El usuario selecciona el archivo de informe HTML exportado de la plataforma original.
2. **Procesamiento mediante MT5HtmlParser:** El sistema lee, limpia y estructura el documento a bajo nivel.
3. **Generación de hash SHA-256:** Se extrae una firma criptográfica única del archivo para blindar su trazabilidad.
4. **Recálculo de métricas:** El motor matemático calcula de forma independiente las métricas financieras (Sortino, Expectancy).
5. **Simulación Monte Carlo:** Se computan 1,000 iteraciones aleatorias de Bootstrap y Shuffle para obtener la Probabilidad de Ruina y el peor Drawdown proyectado.
6. **Evaluación de BacktestValidator:** Aplica los filtros de aceptación cualitativos y cuantitativos para dictar la categoría de la estrategia.
7. **Evaluación del RiskEngine:** Evalúa si la estrategia puede superar las políticas de seguridad paramétricas fundamentales.
8. **Generación automática del informe HTML final:** Se produce un reporte de salida estructurado y visualizable con todo el consolidado de validación, garantizando que el usuario entienda con exactitud la viabilidad y fiabilidad del algoritmo analizado.

### 5.5. Resultados del Proyecto
Con el fin de que se pueda auditar el estado real de los entregables del prototipo en menos de un minuto, se detalla a continuación la tabla consolidada de componentes e indicadores:

| Indicador / Módulo | Estado | Resultado / Observaciones |
| :--- | :---: | :--- |
| **Tests ejecutados** | 117 | Ejecutados de forma automatizada mediante pytest. |
| **Tests superados** | 117 | 100% de los tests superados con éxito. |
| **Tests fallidos** | 0 | Ningún fallo o regresión detectada. |
| **Backend FastAPI** | ✅ Implementado | Servidor API web base y endpoints de validación. |
| **Base de datos SQLite** | ✅ Implementada | Persistencia local inmutable del log de auditoría. |
| **MT5 Parser** | ✅ Implementado | Importador HTML con firmas SHA-256 de integridad. |
| **Metrics Engine** | ✅ Implementado | Recálculo de Sortino, Expectancia y rachas de pérdidas. |
| **Monte Carlo** | ✅ Implementado | Motor estocástico para remuestreo (1,000 iteraciones). |
| **BacktestValidator** | ✅ Implementado | Clasificación lógica de robustez de estrategias. |
| **RiskEngine** | ✅ Implementado | Guardian determinista de 6 reglas operativas de riesgo. |
| **AI Validator Contracts** | ✅ Implementados | Modelos Pydantic abstractos e interfaces de adaptador. |
| **MockAIValidator** | ✅ Implementado | Validador semántico simulado local 100% offline. |
| **Dashboard HTML** | ✅ Implementado | Consola de resultados y reportes unificados. |
| **Demo GUI Interactiva** | ✅ Implementada | Flujo guiado de carga, parsing, validación y reporte. |
| **Ejecución real** | 🔒 Bloqueada | `ALLOW_REAL_EXECUTION=False` insalvable por diseño. |

---

## 6. Desarrollo asistido por IA (Human-in-the-Loop)

Este proyecto ha sido desarrollado bajo un modelo de desarrollo asistido e ingeniería cooperativa, utilizando un enfoque de **Human-in-the-Loop** (Humano en el bucle de decisión), garantizando la calidad arquitectónica del código.

```
       ┌────────────────────────┐
       │   Desarrollador Humano │ (Supervisión y Aprobación Final)
       └────────────────────────┘
         ▲                    ▲
         │                    │
         ▼                    ▼
┌─────────────────┐    ┌────────────────┐
│  Antigravity    │    │ Asistente Dev  │
│  Director IA    │    │  (VS Code)     │
└─────────────────┘    └────────────────┘
```

### 6.1. Antigravity Director (Director IA Antigravity)
Actuó en su rol de **Director del Proyecto y Coordinador Arquitectónico Principal**:
- Dirigió la planificación y estructuración del roadmap técnico.
- Aseguró que cada fase del desarrollo respetara los invariantes de seguridad inquebrantables.
- Validó conceptualmente el diseño de los componentes y la suite de tests.

### 6.2. ChatGPT
Actuó en su rol de **Consultor y Auditor Técnico**:
- Asistió en el diseño de las arquitecturas modulares del sistema.
- Llevó a cabo revisiones de código, refactorizaciones conceptuales y depuración lógica de ecuaciones estadísticas.
- Validó la coherencia de la documentación técnica generada.

### 6.3. VS Code + Cline ( Claude / DeepSeek / Minimax / Qwen )
Actuaron como la **Capa Asistente de Desarrollo Local**:
- Escribieron e implementaron las líneas de código de producción.
- Automatizaron la creación de los tests y la suite de simulación.
- Integraron el routing híbrido de modelos (con OpenRouter) garantizando alta disponibilidad a coste cero.

**Nota de Gobernanza del Desarrollo:**  
Aunque los modelos de IA generaron sugerencias de código y ejecutaron tareas repetitivas, **todas las decisiones técnicas críticas, aprobaciones de arquitecturas de bases de datos e integraciones de seguridad fueron supervisadas y autorizadas de forma explícita por el desarrollador humano**.

---

## 7. KPIs (Key Performance Indicators)

El rendimiento y el valor generado por la infraestructura se miden bajo KPIs específicos divididos en dos áreas de control:

### 7.1. KPIs Técnicos del Laboratorio
- **Pruebas automatizadas ejecutadas:** **117 tests** ejecutados con éxito.
- **Pruebas superadas:** **117 tests** superados.
- **Pruebas fallidas:** **0 tests** fallidos.
- **Latencia de validación de señal:** **< 50ms** en el procesado determinista del `RiskEngine`.
- **Reproducibilidad estocástica:** **100%**. Con el uso de seeds fijadas, dos simulaciones de Monte Carlo sobre el mismo vector de datos arrojan percentiles de drawdown idénticos.
- **Trazabilidad criptográfica:** **100%** de los informes analizados cuentan con su firma SHA-256 persistida en el log de auditoría del laboratorio.

### 7.2. KPIs de Valor de Negocio y Gobernanza
- **Tiempo de validación de un backtest:** Reducción del tiempo de análisis manual de una estrategia de 2 horas a **< 5 segundos**.
- **Estrategias analizadas:** Número acumulado de modelos algorítmicos procesados en la bitácora del laboratorio.
- **Estrategias rechazadas por riesgo:** Cantidad de sistemas descartados automáticamente al superar la probabilidad de ruina umbral (e.g., `risk_of_ruin_pct > 30%`).
- **Estrategias aptas cuantitativamente (Research Approved):** Proporción de sistemas validados con clasificación positiva (`RESEARCH_APPROVED`).
- **Incidencias detectadas antes de despliegue:** Detección de alteraciones o inconsistencias lógicas en el 100% de los informes manipulados.

---

## 8. Gestión de Riesgos

La gobernanza de un laboratorio de validación requiere el control de sus propios riesgos operacionales, descritos en la siguiente matriz de control:

| Riesgo | Probabilidad | Impacto | Mitigación Implementada / Estrategia de Gobernanza |
| :--- | :---: | :---: | :--- |
| **Ejecución Real Accidental** | Muy Baja | Crítico | **Gobernanza de IA:** Bloqueo incondicional en código (`ALLOW_REAL_EXECUTION=False`). El modelo de datos Pydantic lanza una excepción inmediata si `approved_for_real` se intenta instanciar como `True`. |
| **Alucinación de la IA en Coherencia** | Media | Moderado | **Separación de Responsabilidades:** La IA nunca sustituye las decisiones lógicas. Un veredicto de la IA favorable no tiene autoridad para anular un rechazo del `RiskEngine`. |
| **Dependencia de APIs Externas** | Alta | Bajo | **Resiliencia de Infraestructura:** El patrón de adaptadores (`AIValidatorAdapter`) implementa un `MockAIValidator` local que garantiza que el laboratorio siga funcionando al 100% offline si falla internet o la API externa. |
| **Sobreautomatización (Confianza ciega)** | Media | Alto | **Human-in-the-Loop y Riesgo de Automatización Excesiva:** El pipeline incluye una capa final de aprobación interactiva que muestra las razones semánticas de la IA y del motor de riesgos, forzando la intervención del usuario humano. |
| **Sobreajuste del Modelo Analizado** | Muy Alta | Alto | **Validación Estadística:** Se obliga a cada estrategia a pasar el test de remuestreo de **Monte Carlo y Bootstrap**. Las "curvas perfectas" sin robustez estadística son rechazadas automáticamente. |

---

## 9. Plan de implantación

El roadmap técnico de Antigravity sigue un proceso ordenado de hitos para garantizar la estabilidad del software antes de añadir complejidad operativa.

### 9.1. Hitos Alcanzados (Entregables Actuales)
- Implementación completa del backend con FastAPI, Pydantic y SQLite.
- Integración de los motores matemáticos (`MetricsEngine` y `MonteCarlo`) y el parser criptográfico (`MT5HtmlParser`).
- Validación de la arquitectura del validador de IA y los contratos de datos de la **Fase 4.4 completada** (Mock local verificado).
- Generación de la suite de 117 pruebas automatizadas de integración.

### 9.2. Roadmap de Desarrollo (Siguientes Fases)
1. **Fase 4.4B - RemoteAPIValidator:** Sustituir gradualmente el Mock local por llamadas estructuradas a la API de OpenRouter (para DeepSeek Chat, MiniMax, Qwen) y APIs nativas en la nube de Gemini y Claude, implementando persistencia de auditoría en SQLite.
2. **Fase 4.5 - Telegram Approval Layer:** Implementar el bot de mensajería bidireccional que envíe las alertas de validación al teléfono del operador y requiera una respuesta manual obligatoria para continuar en el entorno simulado.
3. **Fase 4.6 - Sandbox de Simulación (Paper Trading) & Gatekeeper MT5:** Integrar de forma directa un webhook para procesar alertas estructuradas de TradingView y enlazarlas a una terminal MetaTrader 5 demo (Gatekeeper), garantizando que las cuentas de simulación operen de forma idéntica a la teoría matemática.
4. **Fase 5 - Kill Switch de Emergencia:** Desarrollo de un endpoint prioritario en FastAPI que apague al instante la recepción de señales en caso de detectar anomalías operativas o comportamientos lógicos inesperados.

---

## 10. Conclusiones

### 10.1. Antigravity no es un Bot de Trading
Es fundamental recalcar que **el Proyecto Antigravity no es un sistema de ejecución automática de operaciones financieras**. Presentar esta solución como un bot de trading convencional desvirtuaría su verdadero propósito académico. 

### 10.2. Infraestructura de Gobernanza y Control
Antigravity es una **infraestructura de gobernanza, auditoría y control de sistemas asistidos por Inteligencia Artificial**. El proyecto demuestra de manera concluyente cómo se puede integrar un modelo cognitivo probabilístico (IA) en procesos de alta responsabilidad, protegiendo al ecosistema de fallos o alucinaciones mediante la aplicación estricta de una arquitectura de software orientada a la **seguridad por diseño** y al enfoque **Human-in-the-Loop**.

A través del pipeline unidireccional desarrollado—que asegura la trazabilidad criptográfica, recalcula de forma aislada las métricas estadísticas, simula estocásticamente la ruina de los modelos y somete toda señal a un motor de riesgo determinista—se entrega una plataforma modular sólida, segura e ideal para la experimentación y el aprendizaje académico responsable en la ingeniería de sistemas complejos asistidos por IA.

---

## Evidencias Visuales del Prototipo

En la versión PDF impresa o distribuida de este informe, se adjuntarán capturas de pantalla de los siguientes elementos del prototipo para verificar el funcionamiento real del sistema:
1. **Arquitectura general de Antigravity:** Diagrama de bloques que demuestra el flujo unidireccional de datos de la solución y las capas de seguridad.
2. **Dashboard HTML:** Vista detallada de la consola de visualización del recálculo matemático de métricas y la distribución estocástica de Monte Carlo.
3. **Demo Académica Interactiva:** Flujo de ejecución interactivo GUI que guía la carga de informes e integra visualmente los módulos de la aplicación.
4. **Informe HTML generado automáticamente:** Reporte compilado de salida que recibe el usuario con las validaciones deterministas e interpretaciones semánticas consolidadas.

Estas evidencias visuales demuestran de manera inequívoca que la infraestructura descrita no es meramente un diseño teórico, sino un desarrollo de software real, operativo e integrable según las metodologías descritas.

---
*Documento preparado y formateado para su presentación académica final ante el tribunal del curso.*  
*approved_for_real = False | ALLOW_REAL_EXECUTION = False*  
*Copyright © 2026. Todos los derechos reservados.*
