import logging
import re

logger = logging.getLogger(__name__)

# Sistema de fallback local baseado em análise de palavras-chave

def classify_email_fallback(text: str):
    try:
        truncated_text = text[:1500] + "..." if len(text) > 1500 else text
        text_lower = truncated_text.lower()
        
        productive_keywords = [
            'problema', 'erro', 'bug', 'falha', 'não funciona', 'quebrado',
            'ajuda', 'suporte', 'socorro', 'urgente', 'importante',
            'dúvida', 'questão', 'pergunta', 'como fazer', 'tutorial',
            'solicitação', 'pedido', 'requisição', 'demanda', 'tarefa',
            'conserto', 'reparo', 'corrigir', 'resolver', 'solucionar',
            'acesso', 'login', 'senha', 'conta', 'sistema', 'aplicativo',
            'técnico', 'assistência', 'orientação', 'instrução'
        ]
        
        unproductive_keywords = [
            'obrigado', 'obrigada', 'agradeço', 'grato', 'gratidão',
            'parabéns', 'congratulações', 'felicitações', 'comemoração',
            'cumprimentos', 'saudações', 'atenciosamente', 'cordialmente', 
            'respeitosamente','abraço', 'abração', 'beijo', 'carinhosamente',
            'confirmado', 'recebido', 'confirmação'
        ]
        
        productive_score = 0
        unproductive_score = 0
        
        for word in productive_keywords:
            if word in text_lower:
                productive_score += 1
                if word in ['problema', 'erro', 'bug', 'urgente', 'suporte', 'requisição', 'ajuda']:
                    productive_score += 2
        
        for word in unproductive_keywords:
            if word in text_lower:
                unproductive_score += 1
                if word in ['obrigado', 'parabéns', 'agradeço']:
                    unproductive_score += 2
        
        has_question = bool(re.search(r'\?|como|porque|por que|qual|quando|onde', text_lower))
        has_thanks = bool(re.search(r'obrigad[oa]|agradeço|grato', text_lower))
        
        if has_question:
            productive_score += 3
        if has_thanks:
            unproductive_score += 2
        
        if productive_score > unproductive_score:
            category = "Produtivo"
            response_text = generate_productive_response(text_lower)
        else:
            category = "Improdutivo"
            response_text = generate_unproductive_response(text_lower)
        
        logger.info(f"Fallback: {category} (P: {productive_score}, I: {unproductive_score})")
        return category, response_text

    except Exception as e:
        logger.error(f"Erro no fallback: {str(e)}")
        return "Produtivo", "Olá! Recebemos sua mensagem e retornaremos em breve."

def generate_productive_response(text: str) -> str:
    responses = [
        "Olá! Obrigado por entrar em contato. Nossa equipe analisará sua solicitação e retornará em breve.",
        "Prezado, agradecemos seu contato. Estamos analisando sua questão e retornaremos em até 24h.",
        "Olá! Recebemos sua solicitação. Nossa equipe técnica já está verificando e em breve teremos uma solução.",
        "Obrigado pelo seu email. Estamos processando sua requisição e retornaremos com informações em breve.",
        "Olá! Sua mensagem foi recebida. Nossa equipe de suporte entrará em contato para resolver sua questão."
    ]
    return responses[len(text) % len(responses)]

def generate_unproductive_response(text: str) -> str:
    responses = [
        "Olá! Agradecemos seu contato e sua mensagem foi recebida com sucesso.",
        "Obrigado por seu email! Apreciamos seu contato e retornaremos se necessário.",
        "Olá! Recebemos sua mensagem. Agradecemos pelo contato e feedback.",
        "Obrigado por entrar em contato! Sua mensagem foi registrada em nosso sistema.",
        "Olá! Agradecemos sua comunicação. Ficamos contentes com seu contato."
    ]
    return responses[len(text) % len(responses)]