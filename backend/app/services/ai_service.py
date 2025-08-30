import logging
import os
from .fallback_service import classify_email_fallback

# Carrega variáveis de ambiente

logger = logging.getLogger(__name__)

# Lê a chave diretamente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def classify_email(text: str):
    logger.info(f"Chave Gemini disponível: {bool(GEMINI_API_KEY)}")
    
    # Tenta Gemini primeiro
    gemini_response = gemini_classification(text)
    if gemini_response:
        return gemini_response
    
    # Se Gemini falhar, usa fallback local
    logger.warning("Usando classificação fallback local!")
    return classify_email_fallback(text)

def gemini_classification(text: str):
    try:
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY não encontrada")
            return None
        
        logger.info("Tentando conectar com Gemini...")
        
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        
        try:
            logger.info(f"Tentando modelo")
            model = genai.GenerativeModel("gemini-2.5-flash")
            logger.info(f"Modelo carregado com sucesso!")
    
        except Exception as model_error:
                logger.warning(f"Modelo falhou: {str(model_error)}")
                
        
        if not model:
            logger.error("Todos os modelos Gemini falharam")
            return None
        
        # Limita o tamanho do texto
        truncated_text = text[:3000] + "..." if len(text) > 3000 else text
        
        # Prompt para classificação
        classification_prompt = f"""
        A sua UNICA tarefa agora é classificar este email.
        Email: {truncated_text}

        Classifique este email como "Produtivo" ou "Improdutivo"

        - "Produtivo": Email que REQUER ação, resposta ou solução (ex: problemas técnicos, dúvidas, solicitações de suporte, pedidos de ajuda, questões urgentes)
        - "Improdutivo": Email que NÃO REQUER ação imediata (ex: agradecimentos, cumprimentos, confirmações, mensagens sociais, felicitações)
        
        EXEMPLOS:
        - "Olá, estou com erro no sistema" = Produtivo
        - "Obrigado pela ajuda!" = Improdutivo  
        - "Como resetar minha senha?" = Produtivo
        - "Parabéns pelo trabalho!" = Improdutivo
        - "Preciso de suporte técnico" = Produtivo
        - "Só queria agradecer" = Improdutivo
        
        Responda APENAS com uma palavra: "Produtivo" ou "Improdutivo".
        """
        
        logger.info("Enviando requisição para classificação...")
        response = model.generate_content(
            classification_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=10,
            )
        )
        
        category = response.text.strip()
        logger.info(f"Resposta bruta do Gemini: '{category}'")
        
        # Normaliza a categoria
        if "produtivo" in category.lower():
            category = "Produtivo"
        elif "improdutivo" in category.lower():
            category = "Improdutivo"
        else:
            logger.warning(f"Resposta inesperada do Gemini: {category}")
            return None
        
        logger.info(f"Categoria normalizada: {category}")
        
        # Geração da resposta
        response_prompt = f"""
        Gere uma resposta profissional breve para um email classificado como {category}.
        Seja direto e educado (máximo 2 frases).
        
        Contexto do email: {truncated_text}
        
        Resposta:
        """
        
        logger.info("Enviando requisição para gerar resposta...")
        response2 = model.generate_content(
            response_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=150,
            )
        )
        
        response_text = response2.text.strip()
        logger.info("Resposta gerada com sucesso pelo Gemini")
        
        return category, response_text
        
    except Exception as e:
        logger.error(f"Erro detalhado no Gemini: {str(e)}")
        logger.error(f"Tipo do erro: {type(e).__name__}")
        return None