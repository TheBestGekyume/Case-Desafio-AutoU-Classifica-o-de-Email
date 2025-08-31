import logging
import random
import re

logger = logging.getLogger(__name__)

PRODUCTIVE_KEYWORDS = {
    'problema': 3, 'erro': 3, 'bug': 3, 'suporte': 3, 'falha': 2,
    'nao funciona': 2, 'quebrado': 2, 'queimado': 2, 'ajuda': 2, 'urgente': 2,
    'projeto': 1, 'socorro': 1, 'importante': 1, 'duvida': 1, 'questao': 1,
    'pergunta': 1, 'como fazer': 1, 'tutorial': 1, 'solicitacao': 1, 'pedido': 1,
    'requisicao': 1, 'demanda': 1, 'tarefa': 1, 'conserto': 1, 'reparo': 1,
    'corrigir': 1, 'resolver': 1, 'solucionar': 1, 'acesso': 1, 'login': 1,
    'senha': 1, 'conta': 1, 'sistema': 1, 'aplicativo': 1, 'tecnico': 1,
    'assistencia': 1, 'orientacao': 1, 'instrucao': 1, 'reuniao': 1
}

UNPRODUCTIVE_KEYWORDS = {
    'parabens': 3, 'beijo': 3, 'abraco': 2, 'promocao': 2, 'carinhosamente': 2,
    'oferta': 2, 'festa': 2, 'aniversario': 2, 'obrigado': 1, 'congratulacoes': 1,
    'felicitacoes': 1, 'cumprimentos': 1, 'saudacoes': 1, 'cordialmente': 1,
    'respeitosamente': 1, 'obrigada': 1, 'abracao': 1, 'gratidão': 1, 'grato': 1,
    'comemoracao': 1, 'confirmado': 1, 'recebido': 1, 'confirmacao': 1, 'agradeco': 1,
}


QUESTION_PATTERN = re.compile(r'\b(como|porque|por que|qual|quando|onde)\b|\?', re.IGNORECASE)
THANKS_PATTERN = re.compile(r'\b(obrigad[oa]|agradeço|grato)\b', re.IGNORECASE)

def classify_email_fallback(text: str, sender: str):
    # logger.error("texto limpo: "+text)

    try:
        SPAM_STRONG_KEYWORDS = ["ganhe dinheiro", "fique milionário", "fique rico",
        "dinheiro fácil", "investimento garantido", "promoção imperdível",
        "oferta exclusiva", "faça fortuna", "multiplique seu dinheiro", 
        "aposta", "pix premiado", "pix milionário", "desconto relâmpago",
        "emagreça rápido", "cura milagrosa"]
        if any(word in text for word in SPAM_STRONG_KEYWORDS):
            category = "Improdutivo"
            response_text = generate_response(category, text, sender)
            return category, response_text

        productive_score = sum(weight for kw, weight in PRODUCTIVE_KEYWORDS.items() if kw in text)
        unproductive_score = sum(weight for kw, weight in UNPRODUCTIVE_KEYWORDS.items() if kw in text)

        if QUESTION_PATTERN.search(text):
            productive_score += 1
        if THANKS_PATTERN.search(text):
            unproductive_score += 1

        if productive_score > unproductive_score:
            category = "Produtivo"
        else:
            category = "Improdutivo"

        response_text = generate_response(category, text, sender)
        logger.info(f"Fallback: {category} (P: {productive_score}, I: {unproductive_score})")
        return category, response_text

    except Exception as e:
        logger.error(f"Erro no fallback: {str(e)}")
        return "Produtivo", f"Olá {sender}! Recebemos sua mensagem e retornaremos em breve."

def generate_response(category: str, text: str, sender: str) -> str:
    productive_responses = [
        f"Olá {sender}! Obrigado por entrar em contato. Nossa equipe analisará sua solicitação e retornará em breve.",
        f"Prezado {sender}, agradecemos seu contato. Estamos analisando sua questão e retornaremos em até 24h.",
        f"Olá {sender}! Recebemos sua solicitação. Nossa equipe técnica já está verificando e em breve teremos uma solução.",
        "Obrigado pelo seu email. Estamos processando sua requisição e retornaremos com informações em breve.",
        f"Olá {sender}! Sua mensagem foi recebida. Nossa equipe de suporte entrará em contato para resolver sua questão."
    ]

    unproductive_responses = [
        f"Olá {sender}! Agradecemos seu contato e sua mensagem foi recebida com sucesso.",
        "Obrigado por seu email! Apreciamos seu contato e retornaremos se necessário.",
        f"Olá {sender}! Recebemos sua mensagem. Agradecemos pelo contato e feedback.",
        "Obrigado por entrar em contato! Sua mensagem foi registrada em nosso sistema.",
        f"Olá {sender}! Agradecemos sua comunicação. Ficamos contentes com seu contato."
    ]

    responses = productive_responses if category == "Produtivo" else unproductive_responses
    return random.choice(responses)
