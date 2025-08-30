import logging
from ..config import GEMINI_API_KEY, HF_API_KEY
from .gemini_service import gemini_classification
from .huggingface_service import huggingface_classification
from .fallback_service import classify_email_fallback

logger = logging.getLogger(__name__)

def classify_email(text: str, sender: str):
    logger.info(f"Iniciando classificação - Texto: {len(text)} chars, Remetente: {sender}")
    logger.info(f"Gemini API disponível: {bool(GEMINI_API_KEY)}")
    logger.info(f"Hugging Face API disponível: {bool(HF_API_KEY)}")
    
    # 1 - Gemini
    if GEMINI_API_KEY:
        logger.info("Tentando classificação com Gemini...")
        result = gemini_classification(text, sender)
        if result:
            category, response_text = result
            logger.info(f"Gemini classificou como: {category}")
            return category, response_text, "gemini"
        else:
            logger.warning("Gemini indisponível no momento")

    # 2 - Hugging Face
    if HF_API_KEY:
        logger.info("Tentando classificação com Hugging Face...")
        result = huggingface_classification(text, sender)
        if result:
            category, response_text = result
            logger.info(f"Hugging Face classificou como: {category}")
            return category, response_text, "huggingface"
        else:
            logger.warning("Hugging Face indisponível no momento")

    # 3 - Fallback local
    logger.info("Usando fallback local...")
    category, response_text = classify_email_fallback(text)
    logger.info(f"Fallback classificou como: {category}")
    return category, response_text, "fallback"