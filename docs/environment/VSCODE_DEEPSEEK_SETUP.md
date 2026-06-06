# Integración VS Code + DeepSeek para Proyecto Antigravity

## Estado: ✅ Funcionando

### Herramientas configuradas
- **Entorno de Dirección Principal:** Google Antigravity (modelos Gemini/Claude nativos para planificación, arquitectura y validación)
- **Entorno de Desarrollo Local Auxiliar:** VS Code
- **IA Asistente local:** Modelos externos de bajo coste (DeepSeek Chat, MiniMax M2) conectados vía OpenRouter

### Flujo de trabajo recomendado

| Tarea | Herramienta |
|-------|-------------|
| Escribir/refactorizar código | VS Code + DeepSeek |
| Depuración rápida | VS Code + DeepSeek |
| Conversaciones largas con historial | Antigravity |
| Comparar con otro modelo (Gemini/Claude) | Antigravity |
| Analizar múltiples archivos | VS Code + DeepSeek |

### Carpetas del proyecto
- Principal: `C:\Users\34628\Downloads\Proyecto_antigravity`
- Curso: `C:\Users\34628\Downloads\Curso_Antigravity`
- Material: `C:\Users\34628\Downloads\Material_clases`

### Configuración de Continue en VS Code
```yaml
models:
  - name: DeepSeek
    provider: openai
    model: deepseek-chat
    apiKey: [TU_API_KEY]
    apiBase: https://api.deepseek.com/v1