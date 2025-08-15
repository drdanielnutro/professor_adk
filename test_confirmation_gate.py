#!/usr/bin/env python
"""
Script de teste para verificar o funcionamento do ConfirmationGateAgent
"""

from app.agent import ConfirmationGateAgent

def test_confirmation_words():
    """Testa se as palavras de confirmação estão configuradas"""
    agent = ConfirmationGateAgent()
    
    print("✅ ConfirmationGateAgent criado com sucesso!")
    print(f"Nome do agente: {agent.name}")
    print(f"Total de palavras de confirmação: {len(agent.CONFIRMATION_WORDS)}")
    print("\nPalavras de confirmação configuradas:")
    for i, word in enumerate(agent.CONFIRMATION_WORDS, 1):
        print(f"  {i:2d}. {word}")
    
    # Testar algumas palavras
    test_cases = [
        ("sim", True),
        ("ok", True),
        ("execute", True),
        ("não", False),
        ("cancelar", False),
        ("sim, pode executar", True),
        ("ok, vamos lá", True),
        ("hmm não sei", False),
    ]
    
    print("\n🧪 Testando detecção de confirmação:")
    for text, expected in test_cases:
        found = any(word in text.lower() for word in agent.CONFIRMATION_WORDS)
        status = "✅" if found == expected else "❌"
        print(f"  {status} '{text}' -> {'Confirmado' if found else 'Não confirmado'}")

if __name__ == "__main__":
    test_confirmation_words()