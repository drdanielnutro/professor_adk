#!/bin/bash
cd "$(dirname "$0")"
echo "🔍 Iniciando ADK Documentation Agent (v2 - Refatorado)..."
echo ""
echo "Este agente busca informações APENAS na documentação oficial do Google ADK"
echo "Disponível em: https://google.github.io/adk-docs/"
echo ""
echo "Estrutura modular inspirada no LLM Auditor 🎯"
echo ""
echo "Escolha o modo de execução:"
echo "1) Interface Web (localhost:8501)"
echo "2) API Server (localhost:8000)"
echo ""
read -p "Digite sua escolha (1 ou 2): " choice

UV_PATH="$HOME/.local/bin/uv"

case $choice in
1)
    echo ""
    echo "🌐 Iniciando interface web em http://localhost:8501"
    echo "Pressione CTRL+C para parar"
    echo ""
    $UV_PATH run python -m google.adk.cli web --port 8501
    ;;
2)
    echo ""
    echo "🔧 Iniciando API server em http://localhost:8000"
    echo "Use com frontend em http://localhost:5173/app/"
    echo "Pressione CTRL+C para parar"
    echo ""
    $UV_PATH run python -m google.adk.cli api_server app --allow_origins="*"
    ;;
*)
    echo "Opção inválida. Execute novamente e escolha 1 ou 2."
    exit 1
    ;;
esac
