from huggingface_hub import InferenceClient
import logging
import re
from ..config import HF_API_KEY

logger = logging.getLogger(__name__)

client = InferenceClient(token=HF_API_KEY)

def huggingface_classification(text: str, sender: str):
    try:
        logger.info(f"Classificando com Hugging Face")
        
        classification_prompt = f"""
        Você trabalha em uma empresa de tecnologia.  
        Classifique este email em "Produtivo" ou "Improdutivo":

        CRITÉRIOS:
        - Produtivo: Pedidos de suporte, resolução de problemas, dúvidas técnicas, solicitações que exigem ação.
        - Improdutivo: Spam, promoções, newsletters, cumprimentos, agradecimentos, convites, festas, sem ação necessária.

        Email: {text}

        LEMBRE-SE, VOCÊ ESTÁ EM UM AMBIENTE PROFISSIONAL.
        Responda APENAS com "Produtivo" ou "Improdutivo".
        """
        
        classification_response = client.chat.completions.create(
            model="meta-llama/Llama-2-7b-chat-hf",
            messages=[
                {"role": "system", "content": "Você é um classificador de e-mails."},
                {"role": "user", "content": classification_prompt}
            ],
            max_tokens=50,
            temperature=0.1
        )

        category = classification_response.choices[0].message["content"].strip()
        category = extract_category(category)
        logger.error(f"Categoria classificada: '{category}'")

        # 2. Gera a resposta baseada na categoria
        response_text = generate_response(category, sender, text)

        return category, response_text

    except Exception as e:
        logger.error(f"Erro no Hugging Face: {str(e)}")
        return None


def extract_category(response: str) -> str:
    text = response.strip().lower()
    if "produtivo" in text:
        return "Produtivo"
    elif "improdutivo" in text:
        return "Improdutivo"
    else:
        return "ERROR"

def generate_response(category: str, sender: str, text: str) -> str:
    logger.info("SENDER = " + sender)
    if category == "Produtivo":
        prompt = f"""
        Gere uma resposta profissional para {sender} informando que:
        - A mensagem foi recebida
        - Foi encaminhada para a equipe responsável e será resolvido
        - Seja breve (1-2 frases)
        - Cite {sender} na mensagem

        Contexto do email: {text[:1000]}

        Escreva o corpo do email, sem assunto e nada além disso!
        """
    else:
        prompt = f"""
        Gere uma resposta educada para {sender} agradecendo o contato,
        mas sem comprometer com ações desnecessárias.
        Seja neutro e breve (1-2 frases).
        
        Contexto do email: {text[:1000]}
        
        Escreva o corpo do email, sem assunto e nada além disso!
        """

    response = client.chat.completions.create(
        model="meta-llama/Llama-2-7b-chat-hf",
        messages=[
            {"role": "system", "content": "Você é um assistente que escreve emails profissionais em português."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    cleaned_response = clean_generated_response(response.choices[0].message["content"])
    logger.info(f"Resposta gerada pelo HF: '{cleaned_response}'")
    return cleaned_response


import re

def clean_generated_response(text: str) -> str:
    
    text = re.sub(r'^\s*(\[.*?\]|Resposta sugerida:|Response:)\s*', '', text, flags=re.IGNORECASE)
    
    text = re.sub(r'["“”]', '', text)
        
    text = text.strip()
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) > 1:
        return ' '.join(sentences[:2]).strip()
    else:
        return text
