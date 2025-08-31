import logging
import string
import re
import nltk
from nltk.corpus import stopwords
from ..config import GEMINI_API_KEY, HF_API_KEY
from .gemini_service import gemini_classification
from .huggingface_service import huggingface_classification
from .fallback_service import classify_email_fallback

logger = logging.getLogger(__name__)

try:
    stop_words = set(stopwords.words("portuguese"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("portuguese"))


def clean_text(text: str, character_limit=3000) -> str:
    if not text or not isinstance(text, str):
        return ""

    processed_text = text.lower()
    processed_text = processed_text.translate(str.maketrans("", "", string.punctuation))
    processed_text = re.sub(r"\s+", " ", processed_text).strip()
    words = [w for w in processed_text.split() if w not in stop_words]
    processed_text = " ".join(words)

    if len(processed_text) > character_limit:
        limit = character_limit - len("...[texto truncado]")
        processed_text = processed_text[:limit].rsplit(" ", 1)[0] + "...[texto truncado]"

    logger.debug(f"Texto limpo: {processed_text[:200]}...")
    return processed_text

# ---------------------
# Função principal
# ---------------------
def classify_email(text: str, sender: str):
    
    logger.info(f"Iniciando classificação - Texto: {len(text)} chars, Remetente: {sender}")

    # Limpa e prepara o texto
    clean_input = clean_text(text)

    logger.info(f"Gemini API disponível: {bool(GEMINI_API_KEY)}")
    logger.info(f"Hugging Face API disponível: {bool(HF_API_KEY)}")

    # 1 - Gemini
    if GEMINI_API_KEY:
        try:
            logger.info("Tentando classificação com Gemini...")
            result = gemini_classification(clean_input, sender)
            if result:
                category, response_text = result
                logger.info(f"Gemini classificou como: {category}")
                return category, response_text, "gemini"
            logger.warning("Gemini indisponível no momento")
        except Exception as e:
            logger.error(f"Erro Gemini: {str(e)}")

    # 2 - Hugging Face
    if HF_API_KEY:
        try:
            logger.info("Tentando classificação com Hugging Face...")
            result = huggingface_classification(clean_input, sender)
            if result:
                category, response_text = result
                logger.info(f"Hugging Face classificou como: {category}")
                return category, response_text, "huggingface"
            logger.warning("Hugging Face indisponível no momento")
        except Exception as e:
            logger.error(f"Erro Hugging Face: {str(e)}")

    # 3 - Fallback local
    logger.info("Usando fallback local...")
    category, response_text = classify_email_fallback(clean_input, sender)
    logger.info(f"Fallback classificou como: {category}")
    return category, response_text, "fallback"
