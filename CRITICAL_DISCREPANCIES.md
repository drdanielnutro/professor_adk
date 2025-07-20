# Discrepâncias Críticas - Deep Research ADK

**Data:** 2025-07-20
**Documentos Comparados:** resposta_claude.md vs resposta_gemini.md

---

## 1. DISCREPÂNCIAS DE NOMENCLATURA

### max_tokens vs max_output_tokens
- **Claude:** Explicitamente corrige: "O parâmetro correto é `max_output_tokens` (não `max_tokens`)"
- **Gemini:** Usa `max_output_tokens` desde o início sem mencionar a confusão comum
- **Impacto:** CRÍTICO - usar `max_tokens` causará erro
- **Ação:** Sempre usar `max_output_tokens`

---

## 2. DISCREPÂNCIAS DE ASSERTIVIDADE

### Posição do ToolContext
- **Claude:** "ToolContext é SEMPRE o último parâmetro"
- **Gemini:** "geralmente é colocado como o último"
- **Realidade:** Claude está correto baseado em todos os exemplos
- **Impacto:** MÉDIO - convenção importante para consistência

### Existência de Atributos
- **Claude:** Lista apenas métodos verificáveis do ToolContext
- **Gemini:** Menciona `tool_context.agent_name` e `.invocation_id`
- **Verificação:** Não encontrados em adk_resumido.json
- **Impacto:** MÉDIO - pode causar AttributeError

---

## 3. DISCREPÂNCIAS DE COMPLETUDE

### Lista de Modelos Gemini
- **Claude:** Lista extensa incluindo GA e preview (2.5-pro, 2.5-flash, 2.0-flash, etc.)
- **Gemini:** Lista parcial (1.5-flash, 1.5-pro, 2.0-flash, 2.5-flash)
- **Diferença:** Claude inclui status GA/preview e mais modelos
- **Impacto:** BAIXO - mais informativo que crítico

### Parâmetros GenerateContentConfig
- **Claude:** Lista 10+ parâmetros com tipos e ranges
- **Gemini:** Menciona apenas básicos (temperature, max_output_tokens, top_p)
- **Diferença:** Claude muito mais completo
- **Impacto:** MÉDIO - desenvolvedores precisam da lista completa

---

## 4. DISCREPÂNCIAS DE IMPLEMENTAÇÃO

### Wrapper Async
- **Claude:** "Não existe wrapper automático. Runtime usa `asyncio.to_thread()`"
- **Gemini:** "Não há wrapper automático" (sem detalhes internos)
- **Diferença:** Claude fornece insight de implementação
- **Impacto:** BAIXO - útil para debugging

### Sistema de Templates
- **Claude:** Foca em InstructionProvider como função Python
- **Gemini:** Destaca também {key} templating simples
- **Diferença:** Abordagens complementares, não conflitantes
- **Impacto:** POSITIVO - mais opções para o desenvolvedor

---

## 5. DISCREPÂNCIAS DE FORMATO

### Estrutura de Testes
- **Claude:** Mostra estruturas JSON específicas (.test.json, .evalset.json)
- **Gemini:** Mostra estrutura JSON genérica não verificável
- **Diferença:** Claude baseado em formato real do ADK
- **Impacto:** ALTO - formato errado não funcionará

### Exemplos de Código
- **Claude:** Código conciso e direto ao ponto
- **Gemini:** Código com mais comentários e contexto
- **Diferença:** Estilo, não substância
- **Impacto:** NEUTRO - questão de preferência

---

## 6. INFORMAÇÕES EXCLUSIVAS

### Apenas no Claude:
1. `asyncio.to_thread()` para execução de sync em runtime async
2. Modelos preview específicos (2.5-flash-lite-preview-06-17)
3. Parâmetros avançados (seed, response_logprobs, cached_content)
4. CallbackChain pattern para múltiplos callbacks

### Apenas no Gemini:
1. {key} templating para interpolação simples
2. Persistência automática via `context.state[key] = value`
3. Menção a ReadonlyContext vs InvocationContext
4. Organização didática de callbacks por nível

---

## 7. CONFLITOS DIRETOS

### Nenhum conflito factual significativo
- Ambas concordam nos pontos fundamentais
- Diferenças são principalmente de:
  - Nível de detalhe
  - Assertividade
  - Completude
  - Estilo de apresentação

---

## RECOMENDAÇÕES DE RECONCILIAÇÃO

### Para Implementação:
1. **Sempre usar** `max_output_tokens` (não max_tokens)
2. **ToolContext** sempre como último parâmetro
3. **Verificar** existência de atributos antes de usar
4. **Testar** modelos específicos antes de assumir disponibilidade

### Para Documentação:
1. **Combinar** abordagens de template (InstructionProvider + {key})
2. **Incluir** tanto exemplos concisos quanto comentados
3. **Mencionar** persistência automática de estado
4. **Organizar** callbacks por nível (agent/model/tool)

### Para Testes:
1. **Usar** formatos .test.json e .evalset.json do Claude
2. **Integrar** com pytest conforme ambos sugerem
3. **Validar** estruturas JSON antes de usar

---

## CONCLUSÃO

As discrepâncias são majoritariamente de **completude e estilo**, não de **correção factual**. A resposta do Claude é mais técnica e assertiva, enquanto a do Gemini é mais didática. Para implementação de produção, priorizar as especificações do Claude com os insights didáticos do Gemini.