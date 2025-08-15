# ADK Documentation Review Agent - Contexto do Projeto

## Visão Geral
Este projeto implementa um agente de documentação refatorado usando o Google ADK (Assistant Development Kit). O agente é especializado em pesquisa e análise de documentação, com foco exclusivo na documentação oficial do ADK em google.github.io/adk-docs/.

## Arquitetura do Sistema

### Estrutura de Arquivos
```
app/
├── __init__.py        # Ponto de entrada exportando root_agent
├── config.py          # Configuração de modelos e ambiente
└── agent.py           # Implementação principal dos agentes
```

## Componentes Principais

### 1. Configuração (config.py)
- **ResearchConfiguration**: Dataclass que define modelos e parâmetros
  - `critic_model`: gemini-2.5-pro (para avaliação)
  - `worker_model`: gemini-2.5-pro (para geração)
  - `max_search_iterations`: 30 (máximo de iterações de busca)
- **Ambiente**: Suporta tanto Vertex AI quanto AI Studio via variáveis de ambiente
- **Autenticação**: Detecta automaticamente credenciais do Google Cloud

### 2. Modelos de Dados Estruturados
- **SearchQuery**: Representa consultas específicas para pesquisa web
- **Feedback**: Modelo para avaliação da qualidade da pesquisa
  - grade: "pass" ou "fail"
  - comment: explicação detalhada
  - follow_up_queries: consultas adicionais se necessário

### 3. Callbacks Especializados
- **collect_research_sources_callback**: Coleta e organiza fontes de pesquisa web
  - Extrai URLs, títulos e domínios
  - Mapeia URLs para IDs curtos (src-N)
  - Armazena claims suportados com scores de confiança
  
- **citation_replacement_callback**: Processa citações no relatório final
  - Converte tags `<cite source="src-N"/>` em links Markdown
  - Mantém formatação e pontuação corretas

### 4. Agentes do Pipeline

#### 4.1 plan_generator
- **Função**: Cria ou refina plano de pesquisa de 5 linhas
- **Classificação de Tarefas**:
  - `[RESEARCH]`: Tarefas de coleta de informações
  - `[DELIVERABLE]`: Tarefas de síntese e criação de outputs
- **Restrição**: Prefixo obrigatório `site:google.github.io/adk-docs/` em todas as buscas

#### 4.2 section_planner
- **Função**: Divide o plano em estrutura markdown com 4-6 seções
- **Output**: Outline organizado do relatório final

#### 4.3 section_researcher
- **Função**: Executa pesquisa web em duas fases
- **Fase 1**: Processa tarefas `[RESEARCH]` com 4-5 queries por objetivo
- **Fase 2**: Processa tarefas `[DELIVERABLE]` usando apenas dados coletados
- **Restrição URL**: Todas as queries devem incluir `site:google.github.io/adk-docs/`

#### 4.4 research_evaluator
- **Função**: Avalia criticamente a qualidade da pesquisa
- **Critérios**: Cobertura, fluxo lógico, fontes, profundidade, clareza
- **Output**: JSON com grade (pass/fail) e queries de follow-up se necessário

#### 4.5 EscalationChecker (Agente Customizado)
- **Função**: Controla o loop de refinamento
- **Lógica**: Escala para parar o loop quando avaliação = "pass"

#### 4.6 enhanced_search_executor
- **Função**: Executa buscas de follow-up quando pesquisa falha
- **Processo**: Executa todas as queries da avaliação e combina com findings existentes

#### 4.7 report_composer
- **Função**: Transforma dados em relatório final com citações
- **Sistema de Citação**: Tags `<cite source="src-ID" />` inline

### 5. Pipeline de Execução

#### research_pipeline (SequentialAgent)
1. section_planner → Cria estrutura do relatório
2. section_researcher → Executa pesquisa inicial
3. LoopAgent (iterative_refinement_loop):
   - research_evaluator → Avalia qualidade
   - escalation_checker → Verifica se deve parar
   - enhanced_search_executor → Refina se necessário
4. report_composer → Gera relatório final com citações

#### interactive_planner_agent (Agente Principal)
- **Workflow**:
  1. Plan: Usa plan_generator para criar plano
  2. Refine: Incorpora feedback do usuário
  3. Execute: Delega para research_pipeline após aprovação
- **Regra Crítica**: Nunca responde diretamente, sempre cria plano primeiro

## Características Especiais

### Restrição de Domínio
- **OBRIGATÓRIO**: Todas as pesquisas são limitadas a `google.github.io/adk-docs/`
- Implementado em todos os agentes de pesquisa
- Prefixo automático em todas as queries

### Sistema de Citações
- Citações inline usando tags especiais
- Conversão automática para links Markdown
- Rastreamento de confiança por claim

### Loop de Refinamento Inteligente
- Avaliação crítica automática
- Refinamento iterativo até qualidade adequada
- Máximo de 30 iterações configurável

## Variáveis de Ambiente Suportadas
- `GOOGLE_GENAI_USE_VERTEXAI`: TRUE/FALSE (escolhe entre Vertex AI e AI Studio)
- `GOOGLE_API_KEY`: Chave da API quando usando AI Studio
- `GOOGLE_CLOUD_PROJECT`: Projeto GCP para Vertex AI
- `GOOGLE_CLOUD_LOCATION`: Região para Vertex AI (padrão: global)

## Estado Atual do Projeto
- Versão refatorada implementada com ADK
- Removidos componentes antigos (callbacks, sub_agents em diretórios separados)
- Consolidado em estrutura mais simples e eficiente
- Foco exclusivo na documentação oficial do ADK

## Notas de Desenvolvimento
- Copyright 2025 Google LLC
- Licenciado sob Apache License 2.0
- Usa modelos Gemini 2.5 Pro para todas as operações
- Suporta thinking mode com pensamentos incluídos
- Callbacks mantêm estado cumulativo durante execução

## Pontos de Entrada
- **Importação Principal**: `from app import root_agent`
- **Agente Root**: `interactive_planner_agent` (alias: `root_agent`)

## Dependências Principais
- google.adk.agents
- google.adk.tools
- google.genai
- pydantic para validação de esquemas
- dotenv para configuração local