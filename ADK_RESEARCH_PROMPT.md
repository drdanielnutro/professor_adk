# PROMPT PARA PESQUISA ADK - PROBLEMA DE TRANSFERÊNCIA EM ORQUESTRADOR

## CONTEXTO DO PROBLEMA

Estou desenvolvendo um sistema multi-agente usando Google ADK que apresenta um problema crítico de fluxo de controle. O orquestrador principal (`interactive_planner_agent`) nem sempre transfere a execução para o pipeline de pesquisa (`research_pipeline`) mesmo quando o usuário confirma explicitamente o plano.

## CÓDIGO ATUAL RELEVANTE

```python
# Estrutura atual do interactive_planner_agent
interactive_planner_agent = LlmAgent(
    name="interactive_planner_agent",
    model=config.worker_model,
    description="The primary research assistant...",
    instruction="""
    Your workflow is:
    1. Plan: Use plan_generator to create a draft plan
    2. Refine: Incorporate user feedback 
    3. Execute: Once user gives EXPLICIT approval (e.g., "looks good, run it"), 
       you MUST delegate to research_pipeline
    """,
    sub_agents=[research_pipeline],
    tools=[AgentTool(plan_generator)],
    output_key="research_plan",
)
```

## COMPORTAMENTO OBSERVADO

### 1. Cenário Problemático
- Usuário fornece tópico de pesquisa
- Agente gera plano usando `plan_generator`
- Usuário confirma com "ok", "sim", "execute"
- **PROBLEMA**: Às vezes o agente responde ao invés de transferir para `research_pipeline`

### 2. Sintomas
- Agente continua conversando em vez de executar
- Não há logs indicando tentativa de transferência
- Pipeline de pesquisa nunca é acionado

## QUESTÕES ESPECÍFICAS PARA PESQUISA

### 1. Mecanismo de Transferência no ADK
- Como o ADK determina quando um `LlmAgent` deve transferir controle para um sub-agente?
- Existe diferença entre `transfer`, `delegate` e `escalate` em termos de implementação?
- Como garantir transferência determinística baseada em condições específicas?

### 2. Padrões de Confirmação de Usuário
- Qual é a melhor prática do ADK para capturar e validar confirmação explícita do usuário?
- É possível interceptar a resposta do usuário antes do LLM processar?
- Como implementar um "gate" de confirmação que força transferência?

### 3. Estado da Sessão e Controle de Fluxo
- Como acessar `ctx.session.state` para verificar mensagens do usuário?
- É possível criar um `BaseAgent` customizado que valida confirmação antes de permitir transferência?
- Como os callbacks podem influenciar decisões de transferência?

### 4. Arquitetura de Solução
- Devo criar um agente intermediário entre `interactive_planner` e `research_pipeline`?
- É melhor usar `SequentialAgent` com um agente de validação?
- Como implementar um padrão "confirmation gate" no ADK?

## CÓDIGO DE EXEMPLO PARA ANÁLISE

```python
# Proposta de solução sugerida (precisa validação)
class ConfirmationGateAgent(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext):
        user_input = ctx.session.state.get("last_user_message")
        confirmation_words = ["sim", "ok", "execute", "faça", "prossiga"]
        
        if any(word in user_input.lower() for word in confirmation_words):
            yield Event(
                author=self.name,
                actions=EventActions(transfer="research_pipeline")
            )
        else:
            yield Event(
                author=self.name,
                actions=EventActions(request_input="Por favor confirme...")
            )
```

## REQUISITOS DA SOLUÇÃO

1. **Garantia de Transferência**: 100% de confiabilidade quando usuário confirma
2. **Palavras de Confirmação**: "sim", "ok", "pode", "execute", "faça isso", "prossiga"
3. **Rastreabilidade**: Logs claros mostrando decisão de transferência
4. **Compatibilidade**: Solução deve funcionar com estrutura ADK existente

## PERGUNTAS CRÍTICAS

1. **Como forçar um `LlmAgent` a sempre transferir controle quando detecta palavras específicas de confirmação?**

2. **Existe um padrão oficial do ADK para implementar "user confirmation gates"?**

3. **Como debugar/rastrear decisões de transferência do orquestrador?**

4. **Qual é a diferença prática entre usar `transfer` no EventActions vs. usar `AgentTool` com sub_agents?**

5. **É possível sobrescrever o comportamento de decisão do LLM com lógica determinística para casos específicos?**

## CONTEXTO ADICIONAL

- Usando ADK versão mais recente
- Sistema multi-agente com pipeline de pesquisa complexo
- Necessidade de controle determinístico sobre fluxo de execução
- Usuários relatam que sistema "não executa" mesmo após confirmação

## SOLICITAÇÃO DE ANÁLISE

Por favor, forneça:

1. **Análise Técnica Detalhada**
   - Explicação de como o ADK processa decisões de transferência internamente
   - Identificação da causa raiz do problema
   - Análise dos pontos de falha possíveis

2. **Solução Recomendada com Código**
   - Implementação completa e testada
   - Explicação passo a passo
   - Considerações de edge cases

3. **Melhores Práticas**
   - Padrões recomendados para confirmation gates
   - Técnicas de debugging para fluxo de agentes
   - Estratégias de logging e monitoramento

4. **Alternativas e Trade-offs**
   - Diferentes abordagens possíveis
   - Prós e contras de cada solução
   - Recomendação final baseada no contexto

## INFORMAÇÕES ADICIONAIS DO SISTEMA

### Estrutura do Projeto
```
adk-review-docs/
├── app/
│   ├── agent.py           # Orquestrador principal
│   ├── config.py          # Configurações
│   └── callbacks/         # Callbacks customizados
└── pyproject.toml         # Dependências
```

### Fluxo Esperado
1. Usuário: "Pesquise sobre [tópico]"
2. Sistema: Gera plano com `plan_generator`
3. Sistema: Apresenta plano ao usuário
4. Usuário: "Ok, execute"
5. Sistema: **DEVE** transferir para `research_pipeline`
6. Pipeline: Executa pesquisa completa

### Problema Principal
Entre os passos 4 e 5, a transferência nem sempre ocorre, mesmo com confirmação explícita do usuário.