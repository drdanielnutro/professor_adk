# ADK Documentation Agent v2 (Refatorado)

Um agente especializado em buscar informações exclusivamente na documentação oficial do Google Agent Development Kit (ADK).

**✨ Esta é a versão refatorada com estrutura modular inspirada no LLM Auditor, mantendo toda a sofisticação técnica do agente original.**

## 🎯 Objetivo

Este agente foi criado para responder perguntas sobre o Google ADK consultando APENAS a documentação oficial em https://google.github.io/adk-docs/, garantindo respostas precisas e confiáveis sobre:

- Arquitetura e classes do ADK
- Como criar agentes customizados
- Sistema de tools e callbacks
- Melhores práticas de desenvolvimento
- Configuração e deployment

## 📁 Estrutura do Projeto

```
adk-docs-agent-v2/
├── Makefile                  # Comandos de build e execução
├── README.md                 # Este arquivo
├── pyproject.toml            # Dependências e configurações do projeto
├── run_agent.sh              # Script de execução simplificado
├── uv.lock                   # Lock file das dependências
└── app/                      # Código principal do agente
    ├── __init__.py
    ├── agent.py              # Orquestração principal (75 linhas!)
    ├── config.py             # Configurações do agente
    ├── .env                  # Variáveis de ambiente (não versionado)
    ├── callbacks/            # Callbacks modulares
    │   ├── __init__.py
    │   └── research_callbacks.py
    └── sub_agents/           # Subagentes organizados modularmente
        ├── __init__.py
        ├── enhanced_search/  # Busca aprimorada para refinamento
        │   ├── __init__.py
        │   └── agent.py
        ├── escalation/       # Controle de loop iterativo
        │   ├── __init__.py
        │   └── agent.py
        ├── evaluator/        # Avaliação crítica da pesquisa
        │   ├── __init__.py
        │   └── agent.py
        ├── planner/          # Planejador de pesquisa
        │   ├── __init__.py
        │   ├── agent.py
        │   └── prompt.py
        ├── researcher/       # Pesquisador principal
        │   ├── __init__.py
        │   ├── agent.py
        │   └── prompt.py
        ├── section_planner/  # Planejador de estrutura
        │   ├── __init__.py
        │   └── agent.py
        └── writer/           # Compositor de relatórios
            ├── __init__.py
            ├── agent.py
            └── prompt.py
```

## 🚀 Como Usar

### Pré-requisitos
- Python 3.10+
- uv (gerenciador de pacotes)
- Google AI Studio API Key

### Instalação

1. Navegue até o diretório do agente:
```bash
cd /Users/institutorecriare/VSCodeProjects/professor_adk/adk-review-docs
```

2. Instale as dependências:
```bash
make install
```

### Execução

#### Usando o script simplificado:
```bash
./run_agent.sh
```

#### Ou diretamente com Make:

**Opção 1: Interface Web (Recomendado para testes)**
```bash
make playground
```
Acesse http://localhost:8501

**Opção 2: API Server**
```bash
make dev
```
Use com o frontend do gemini-fullstack em http://localhost:5173/app/

## 🔧 Como Funciona

### Arquitetura Modular
Este agente foi refatorado para seguir a estrutura modular do LLM Auditor, mas mantendo toda a sofisticação do ADK Docs Agent original:

- **Separação de responsabilidades**: Cada subagente em seu próprio módulo
- **Prompts isolados**: Arquivos `prompt.py` dedicados para prompts longos
- **Callbacks organizados**: Callbacks complexos em módulo separado

### Sistema de Busca
O agente garante buscas exclusivas na documentação ADK através de instruções nos prompts. Todos os agentes são instruídos a adicionar o filtro `site:google.github.io/adk-docs/` antes de cada query ao usar a ferramenta `google_search`.

### Fluxo de Execução
1. **Planejamento**: `plan_generator` cria um plano de pesquisa
2. **Estruturação**: `section_planner` organiza o relatório em seções
3. **Pesquisa**: `section_researcher` executa pesquisas profundas
4. **Avaliação**: `research_evaluator` verifica a qualidade
5. **Refinamento**: Loop iterativo até aprovação (máx 3 iterações)
6. **Composição**: `report_composer` gera o relatório final com citações

### Agentes Especializados
- **plan_generator**: Cria planos de pesquisa focados em ADK
- **section_planner**: Estrutura o relatório em seções markdown
- **section_researcher**: Executa pesquisas exclusivamente nos docs oficiais
- **research_evaluator**: Avalia criticamente a qualidade da pesquisa
- **report_composer**: Compõe o relatório final com citações formatadas
- **EscalationChecker**: Controla o loop de refinamento
- **enhanced_search_executor**: Executa buscas de refinamento quando necessário

## 📝 Exemplos de Uso

```
"Como criar um agente customizado no ADK?"
"Quais são as principais classes do ADK Python?"
"Como implementar callbacks em agentes ADK?"
"Explique o sistema de tools do ADK"
"Como fazer deploy de um agente ADK no Vertex AI?"
```

## 🐛 Correção Importante

Este agente já inclui a correção para o bug de carregamento do arquivo `.env`. Se você encontrar o erro de credenciais, verifique se:
1. O arquivo `app/.env` existe e contém suas chaves
2. `python-dotenv` está instalado
3. O `config.py` está carregando o `.env` corretamente

## 🔍 Diferenças da Versão Original

### Em relação ao ADK Docs Agent v1:
1. **Estrutura Modular**: De 437 linhas em um arquivo para múltiplos módulos organizados
2. **Manutenibilidade**: Cada componente em seu lugar apropriado
3. **Escalabilidade**: Fácil adicionar novos subagentes ou ferramentas
4. **Clareza**: Agent.py principal com apenas 75 linhas de orquestração

### Mantém do original:
1. **Busca Restrita**: Todas as pesquisas filtradas para docs oficiais
2. **Sofisticação Técnica**: Loops, callbacks avançados, avaliação iterativa
3. **Qualidade**: Mesmo nível de resposta detalhada e citada
4. **Funcionalidade**: 100% compatível com o agente original

## 📚 Recursos Adicionais

- [Documentação Oficial do ADK](https://google.github.io/adk-docs/)
- [Repositório do ADK Python](https://github.com/google/adk-python)
- [Samples do ADK](https://github.com/google/adk-samples)