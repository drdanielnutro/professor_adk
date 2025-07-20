# Escalation Checker Agent

Este agente é uma implementação customizada de `BaseAgent` que não requer prompt.

## Por que não tem prompt.py?

O EscalationChecker é um agente de controle de fluxo que:
- Não usa LLM para processar texto
- Apenas verifica uma condição (grade == "pass")
- Executa lógica programática, não processamento de linguagem natural

Portanto, não há necessidade de um arquivo `prompt.py` separado, pois não há instruções em linguagem natural para separar do código.

## Função

O agente verifica o resultado da avaliação de pesquisa e:
- Se `grade == "pass"`: Escala para parar o loop iterativo
- Se `grade == "fail"`: Permite que o loop continue para refinamento