import logging
import google.generativeai as genai
from ..config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

def gemini_classification(text: str, sender: str):
    try:
            
        logger.info("Tentando conectar com Gemini...")
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        try:
            logger.info("Tentando modelo gemini-1.5-flash-latest")
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            logger.info("Modelo carregado com sucesso!")
        except Exception as model_error:
            logger.warning(f"Modelo falhou: {str(model_error)}")
            return None
                
        
        classification_prompt = f"""
        Você trabalha em uma empresa de tecnologia.  
        Classifique este email em "Produtivo" ou "Improdutivo":

        CRITÉRIOS:
        - Produtivo: Pedidos de suporte, resolução de problemas, dúvidas técnicas, solicitações que exigem ação.
        - Improdutivo: Spam, promoções, newsletters, cumprimentos, agradecimentos, sem ação necessária.

        Email: {text}

        Responda APENAS com "Produtivo" ou "Improdutivo".
        """
        
        logger.info("Enviando requisição para classificação...")
        classification_response = model.generate_content(
            classification_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=10,
            )
        )
        
        # Extrai a categoria da resposta
        category = extract_response(classification_response).strip()
        
        logger.info(f"Categoria classificada: '{category}'")
        
        response_text = generate_response(category, sender, text, model)
        
        return category, response_text
        
    except Exception as e:
        logger.error(f"Erro no Gemini: {str(e)}")
        logger.error(f"Tipo do erro: {type(e).__name__}")
        return None

def extract_response(response):
    if hasattr(response, 'text'):
        return response.text
    elif hasattr(response, 'parts') and response.parts:
        return response.parts[0].text
    elif hasattr(response, 'candidates') and response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return ""

def generate_response(category: str, sender: str, text: str, model):
    if category == "Produtivo":
        prompt = f"""
        Gere uma resposta profissional para {sender} informando que:
        - A mensagem foi recebida
        - Foi encaminhada para a equipe responsável
        - Serão tomadas providências
        - Seja breve (1-2 frases)
        Contexto: {text}
        """
    else:
        prompt = f"""
        Você é um funcionario de uma empresa de tecnologia
        esse email improdutivo:{text}

        Gere uma resposta profissional para {sender}.
        Seja neutro e breve (1 frases).
        Não aceite ou recuse nada.
        Lembre-se, você esta respondendo pela empresa, não por você mesmo.
        """
    
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.5,
            max_output_tokens=100,
        )
    )
    
    return extract_response(response).strip()