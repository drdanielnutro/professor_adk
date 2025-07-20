# Matriz de Decisão - Deep Research ADK

**Data:** 2025-07-20
**Objetivo:** Definir qual resposta usar para cada correção necessária

---

## Matriz de Decisão Detalhada

| # | Tópico | Claude | Gemini | Decisão | Justificativa |
|---|--------|---------|---------|----------|--------------|
| 1 | **FunctionTool - Parâmetros** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **CLAUDE** | Exemplo mais completo, mostra auto-wrapping |
| 2 | **Funções Async** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **CLAUDE** | Menciona `asyncio.to_thread()`, mais técnico |
| 3 | **GenerateContentConfig** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **CLAUDE** | Lista completa de parâmetros + correção crítica |
| 4 | **Templates/InstructionProvider** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **AMBAS** | Claude: técnico, Gemini: {key} templating |
| 5 | **Framework de Testes** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **CLAUDE** | Formatos .test.json e .evalset.json precisos |
| 6 | **Modelos Gemini** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **CLAUDE** | Lista assertiva com GA/preview status |
| 7 | **Estado de Sessão** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **AMBAS** | Gemini: persistência automática importante |
| 8 | **Imports/Módulos** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **CLAUDE** | Lista completa organizada por categoria |
| 9 | **ToolContext** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **CLAUDE** | Métodos verificados, posição assertiva |
| 10 | **Callbacks** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **CLAUDE** | Assinaturas precisas com tipos |

**Pontuação Total:** Claude 48/50 | Gemini 38/50

---

## Informações Complementares do Gemini

### Valiosas para Incluir:
1. **{key} Templating** - Interpolação simples de estado em instruções
2. **Persistência Automática** - `context.state[key] = value` persiste automaticamente
3. **Organização de Callbacks por Nível** - Didática clara agent/model/tool
4. **ReadonlyContext** - Menção explícita para InstructionProvider

### Ignorar do Gemini:
1. Atributos não verificáveis (`tool_context.agent_name`)
2. Estruturas JSON de teste não confirmadas
3. Afirmações menos assertivas sobre posições

---

## Plano de Uso por Arquivo

### architecture.json
- **Base:** Resposta Claude
- **Correções:**
  - `max_tokens` → `max_output_tokens`
  - Remover `name` e `description` de FunctionTool
  - Confirmar modelo `gemini-2.5-flash`

### implementation.py
- **Base:** Resposta Claude
- **Correções:**
  - Converter funções async para sync OU
  - Migrar para LongRunningFunctionTool
  - ToolContext sempre como último parâmetro

### templates.jinja
- **Base:** Ambas respostas
- **Implementação:**
  - Opção A: InstructionProvider Python (Claude)
  - Opção B: {key} templating simples (Gemini)
  - Decidir baseado em complexidade necessária

### tests.yaml
- **Base:** Resposta Claude
- **Conversão:**
  - Formato .test.json para testes unitários
  - Formato .evalset.json para testes de sessão
  - Integração com pytest

---

## Código de Referência Consolidado

### 1. FunctionTool Correto (Claude)
```python
def get_weather(city: str) -> dict:
    """Retrieves current weather for a city."""
    return {"status": "success", "report": "Sunny, 25°C"}

# ADK converte automaticamente
agent = Agent(tools=[get_weather])
```

### 2. LongRunningFunctionTool (Claude)
```python
def slow_analysis(data: str):
    """Generator function for long operations"""
    yield {"status": "initializing"}
    # processing...
    return {"status": "completed"}

tool = LongRunningFunctionTool(func=slow_analysis)
```

### 3. GenerateContentConfig (Claude)
```python
config = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=1024,  # NÃO max_tokens!
    top_p=0.95,
    frequency_penalty=0.1,
    presence_penalty=0.1
)
```

### 4. InstructionProvider (Ambas)
```python
# Método Claude - Função completa
def dynamic_instruction(context: ReadonlyContext) -> str:
    return f"Usuário: {context.state.get('user:name')}"

# Método Gemini - String template
instruction = "Olá {user:name}, como posso ajudar?"
```

---

## Decisão Final

**Usar resposta Claude como base principal** com os seguintes complementos do Gemini:
1. Mencionar {key} templating como alternativa simples
2. Enfatizar persistência automática de estado
3. Incluir organização didática de callbacks

**Razão:** Claude demonstrou maior precisão técnica, assertividade e exemplos verificáveis contra adk_resumido.json.