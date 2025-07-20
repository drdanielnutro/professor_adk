# Plano de Modificação - Arquivos Professor ADK

**Data:** 2025-07-20
**Base:** Deep Research validada (principalmente resposta Claude)
**Prioridade:** Correções críticas primeiro, melhorias depois

---

## 📋 RESUMO DAS MODIFICAÇÕES

### Arquivos a Modificar:
1. **architecture.json** - 5 correções críticas
2. **implementation.py** - 3 correções críticas + 2 melhorias
3. **templates.jinja** - Conversão completa para Python
4. **tests.yaml** - Conversão completa para JSON

---

## 📁 ARQUIVO 1: architecture.json

### CORREÇÃO 1.1: max_output_tokens (CRÍTICO)
**Localização:** Linha 19
```json
// ANTES:
"max_tokens": 1000

// DEPOIS:
"max_output_tokens": 1000
```

### CORREÇÃO 1.2: Parâmetros FunctionTool (CRÍTICO)
**Localização:** Linhas 35-37, 47-49, 59-61, 71-73
```json
// ANTES:
"configuracao": {
  "func": "transcrever_audio",
  "name": "transcrever_audio",
  "description": "Transcreve arquivo de áudio completo para texto"
}

// DEPOIS:
"configuracao": {
  "func": "transcrever_audio"
  // name e description serão extraídos da docstring
}
```

### CORREÇÃO 1.3: Modelo Gemini (IMPORTANTE)
**Localização:** Linha 9
```json
// VERIFICAR se gemini-2.5-flash está disponível
// Se não, mudar para:
"model": "gemini-2.0-flash"
```

### CORREÇÃO 1.4: Remover patterns não ADK (LIMPEZA)
**Localização:** Linhas 22-26
```json
// REMOVER bloco "patterns" - não faz parte do ADK
```

### CORREÇÃO 1.5: Adicionar response_mime_type (MELHORIA)
**Localização:** Dentro de generate_content_config
```json
"generate_content_config": {
  "temperature": 0.7,
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain"  // ADICIONAR
}
```

---

## 📁 ARQUIVO 2: implementation.py

### CORREÇÃO 2.1: Remover async das funções (CRÍTICO)
**Localização:** Linhas 34, 96, 158, 232
```python
# ANTES:
async def transcrever_audio(
    audio_data: str,
    formato: str,
    tool_context: ToolContext
) -> Dict[str, Any]:

# DEPOIS:
def transcrever_audio(
    audio_data: str,
    formato: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
```

### CORREÇÃO 2.2: Adicionar docstrings completas (CRÍTICO)
**Todas as funções devem ter docstrings no formato:**
```python
def nome_funcao(params):
    """Descrição breve da ferramenta (será o description).
    
    Descrição mais detalhada se necessário.
    
    Args:
        param1: Descrição do parâmetro
        param2: Descrição do parâmetro
        tool_context: Contexto da ferramenta ADK
        
    Returns:
        Dict com estrutura esperada
    """
```

### CORREÇÃO 2.3: Import correto do ADK (IMPORTANTE)
**Localização:** Linha 13
```python
# ANTES:
from google.adk.tools import ToolContext

# DEPOIS:
from google.adk.tools import ToolContext, FunctionTool
from google.adk.agents import LlmAgent
```

### MELHORIA 2.4: Adicionar validação de tool_context
```python
def transcrever_audio(..., tool_context: ToolContext) -> Dict[str, Any]:
    # ADICIONAR no início:
    if tool_context and hasattr(tool_context, 'state'):
        # Log ou rastrear uso da ferramenta
        tool_context.state['temp:last_tool_used'] = 'transcrever_audio'
```

### MELHORIA 2.5: Padronizar estrutura de retorno
```python
# Criar classe base para respostas consistentes:
@dataclass
class ToolResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }
```

---

## 📁 ARQUIVO 3: templates.jinja → templates.py

### CONVERSÃO 3.1: Criar instruction_providers.py
**Novo arquivo com InstructionProviders Python:**

```python
from google.adk.agents.readonly_context import ReadonlyContext
from typing import Optional

def professor_instruction_provider(context: ReadonlyContext) -> str:
    """Gera instrução dinâmica para o Professor Virtual."""
    
    # Extrair dados do contexto
    user_name = context.state.get("user:name", "")
    serie_escolar = context.state.get("user:serie_escolar", "")
    historico_count = len(context.state.get("user:historico_duvidas", []))
    
    # Construir instrução base
    instruction = """Você é o Professor Virtual, um assistente educacional especializado em ajudar crianças com suas dúvidas escolares. Sua missão é fornecer explicações claras, encorajadoras e apropriadas para a idade.

## Contexto da Sessão"""
    
    if user_name:
        instruction += f"\n- Nome do aluno: {user_name}"
    if serie_escolar:
        instruction += f"\n- Série escolar: {serie_escolar}"
    if historico_count > 0:
        instruction += f"\n- Histórico recente: {historico_count} dúvidas respondidas"
    
    # Adicionar diretrizes
    instruction += """

## Diretrizes para Resposta

1. **Linguagem Apropriada**: Use linguagem simples e amigável
2. **Estrutura Clara**: Organize em passos quando apropriado
3. **Encorajamento**: Sempre inclua palavras de motivação
4. **Exemplos Práticos**: Use exemplos do dia a dia
5. **Verificação**: Termine perguntando se entendeu"""
    
    return instruction

# Criar providers para cada template original
def erro_instruction_provider(context: ReadonlyContext) -> str:
    tipo_erro = context.state.get("temp:tipo_erro", "processar")
    # ... implementar lógica do template
```

### CONVERSÃO 3.2: Alternativa com {key} templating
**Para templates simples, usar interpolação direta:**
```python
# Em agent.py:
welcome_instruction = """
Olá {user:name}! Eu sou o Professor Virtual! 🎓
Estou aqui para ajudar você com suas tarefas da {user:serie_escolar}.
"""
```

---

## 📁 ARQUIVO 4: tests.yaml → tests/

### CONVERSÃO 4.1: Criar estrutura de testes
```
tests/
├── unit/
│   ├── basic_questions.test.json
│   └── visual_detection.test.json
├── integration/
│   ├── full_flow.evalset.json
│   └── error_handling.evalset.json
└── test_agent.py
```

### CONVERSÃO 4.2: Exemplo de .test.json
```json
[
  {
    "query": "O que é fotossíntese?",
    "expected_tool_use": [
      {
        "tool_name": "transcrever_audio",
        "tool_input": {
          "audio_data": "AUDIO_BASE64",
          "formato": "mp3"
        }
      }
    ],
    "expected_response_contains": ["plantas", "luz", "energia"]
  }
]
```

### CONVERSÃO 4.3: Integração pytest
```python
# test_agent.py
import pytest
from google.adk.evaluation import AgentEvaluator

@pytest.mark.asyncio
async def test_professor_basic():
    await AgentEvaluator.evaluate(
        agent_module="app.agent",
        eval_dataset_file_path_or_dir="tests/unit/"
    )
```

---

## 🚀 ORDEM DE EXECUÇÃO

### Fase 1: Correções Críticas (Bloqueantes)
1. [ ] architecture.json - max_output_tokens
2. [ ] architecture.json - remover name/description de FunctionTool
3. [ ] implementation.py - remover async de todas as funções
4. [ ] implementation.py - garantir docstrings completas

### Fase 2: Estrutura de Templates
5. [ ] Criar instruction_providers.py
6. [ ] Converter templates Jinja para Python
7. [ ] Atualizar agent.py para usar providers

### Fase 3: Framework de Testes
8. [ ] Criar estrutura de diretórios tests/
9. [ ] Converter YAML para JSON
10. [ ] Implementar pytest integration

### Fase 4: Melhorias e Polimento
11. [ ] Adicionar validações em tool_context
12. [ ] Implementar ToolResponse padrão
13. [ ] Adicionar response_mime_type
14. [ ] Documentar mudanças

---

## ✅ CRITÉRIOS DE VALIDAÇÃO

### Após cada fase, validar:
1. **Import test:** `python -c "from app import agent"`
2. **Syntax check:** `python -m py_compile arquivo.py`
3. **ADK compliance:** Comparar com exemplos da documentação

### Teste final:
```bash
# Executar um teste simples
uv run python -c "
from app.agent import professor_virtual
print('Agent loaded:', professor_virtual.name)
"
```

---

## 📝 NOTAS IMPORTANTES

1. **Backup primeiro:** Copiar todos os arquivos originais
2. **Commits incrementais:** Um commit por correção
3. **Testar após cada mudança:** Não acumular erros
4. **Documentar decisões:** Explicar no commit porque cada mudança

---

## 🎯 RESULTADO ESPERADO

Após todas as modificações:
- ✅ Código 100% compatível com ADK
- ✅ Sem warnings ou deprecations
- ✅ Testes automatizados funcionando
- ✅ Templates dinâmicos e manuteníveis
- ✅ Estrutura pronta para produção