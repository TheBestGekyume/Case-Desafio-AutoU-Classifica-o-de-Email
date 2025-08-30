import logging
import os
import textwrap
from .fallback_service import classify_email_fallback

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
            logger.info("Tentando modelo gemini-1.5-flash-latest")
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            logger.info("Modelo carregado com sucesso!")
        except Exception as model_error:
            logger.warning(f"Modelo falhou: {str(model_error)}")
            return None
        
        # Limita o tamanho do texto
        truncated_text = text[:3000] + "..." if len(text) > 3000 else text
        
        # Prompt para classificação
        classification_prompt = f"""
        Você trabalha em uma empresa de tecnologia.  
        Os emails recebidos podem ser internos (entre colegas) ou externos (de clientes).  

        Classes possíveis:  
        - "Produtivo": São mensagens que pedem suporte, resolução de problemas, dúvidas de clientes, solicitações diretas, ou informações que exigem acompanhamento.  
        - "Improdutivo": São mensagens de propaganda, spam, promoções, cumprimentos, agradecimentos, convites, ou qualquer mensagem que NÃO exige resposta ou ação real. 

        Email: {truncated_text}

        Responda APENAS com "Produtivo" ou "Improdutivo".
        """
        
        logger.info("Enviando requisição para classificação...")
        response = model.generate_content(
            classification_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=10,
            )
        )
        
        if hasattr(response, 'text'):
            category = response.text.strip()
        elif hasattr(response, 'parts') and response.parts:
            category = response.parts[0].text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            category = response.candidates[0].content.parts[0].text.strip()
        else:
            logger.error("Não foi possível extrair texto da resposta")
            return None
        
        logger.info(f"Resposta bruta do Gemini: '{category}'")
                
        # Geração da resposta
        if category == "Produtivo":
            response_prompt = f"""
            Você está respondendo diretamente esse email.
            A resposta deve:
            - Não resolver o problema diretamente
            - Apenas informar que a mensagem foi recebida e encaminhada para a equipe responsável
            - Ser educada e profissional
            - Ter no máximo 1 ou 2 frases

            Email: {truncated_text}

            Resposta:
            """
        else:
            response_prompt = f"""
            Você classificou o email como IMPRODUTIVO.
            Gere uma resposta educada e breve (máximo 2 frases),
            reconhecendo o recebimento, mas sem dar continuidade desnecessária
            seja neutro.

            Contexto do email: {truncated_text}

            Resposta:
            """

        response_prompt = textwrap.dedent(response_prompt)
        
        logger.info("Enviando requisição para gerar resposta...")
        response2 = model.generate_content(
            response_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=100,
            )
        )
        
        # CORREÇÃO: Acessa a resposta corretamente
        if hasattr(response2, 'text'):
            response_text = response2.text.strip()
        elif hasattr(response2, 'parts') and response2.parts:
            response_text = response2.parts[0].text.strip()
        elif hasattr(response2, 'candidates') and response2.candidates:
            response_text = response2.candidates[0].content.parts[0].text.strip()
        else:
            response_text = "Olá! Agradecemos seu contato."
        
        logger.info("Resposta gerada com sucesso pelo Gemini")
        
        return category, response_text
        
    except Exception as e:
        logger.error(f"Erro detalhado no Gemini: {str(e)}")
        logger.error(f"Tipo do erro: {type(e).__name__}")
        return None