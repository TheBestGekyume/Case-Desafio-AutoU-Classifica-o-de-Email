import string
import re
import nltk
from nltk.corpus import stopwords
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging

from app.services.classify_service import classify_email
from ..services.file_service import extract_file_content 

router = APIRouter()
logger = logging.getLogger(__name__)

try:
    stop_words = set(stopwords.words('portuguese'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('portuguese'))

def clean_text(text, character_limit=3000):
     
    if not text or not isinstance(text, str):
        return ""
    
    processed_text = text.lower()
    processed_text = processed_text.translate(str.maketrans('', '', string.punctuation))
    
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    
    palavras = processed_text.split()
    palavras_filtradas = [palavra for palavra in palavras if palavra not in stop_words]
    processed_text = " ".join(palavras_filtradas)
    
    if len(processed_text) > character_limit:
        real_character_limit = character_limit - len("...[texto truncado]")
        processed_text = processed_text[:real_character_limit].rsplit(' ', 1)[0] + "...[texto truncado]"

    logger.debug(f"Texto limpo: {processed_text[:200]}...") 

    return processed_text


@router.post("/classify")
async def classify_email_route(
    sender: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        file_text = ""
        extracted_sender = None
        extracted_subject = None
        extracted_message = None
        
        if file and file.filename:
            file_text, extracted_sender, extracted_subject, extracted_message = await extract_file_content(file)
            logger.info(f"Conteúdo extraído do arquivo: {len(file_text)} caracteres")

        # Usar informações extraídas do arquivo se disponíveis
        final_sender = sender or extracted_sender
        final_subject = subject or extracted_subject
        final_message = message or extracted_message

        # Verificar se temos conteúdo suficiente
        if not file_text and (not final_subject or not final_message):
            raise HTTPException(
                status_code=400, 
                detail="Envie um arquivo ou preencha subject e message."
            )

        if file_text:
            full_text = file_text
        else:
            full_text_parts = []
            if final_sender:
                full_text_parts.append(f"Remetente: {final_sender}")
            if final_subject:
                full_text_parts.append(f"Assunto: {final_subject}")
            if final_message:
                full_text_parts.append(f"Mensagem: {final_message}")
            full_text = "\n".join(full_text_parts)

        logger.info(f"Texto para classificação: {len(full_text)} caracteres")
        logger.info(f"Remetente: {final_sender}")
        logger.info(f"Assunto: {final_subject}")

        full_text = clean_text(full_text)

        category, response_text, source = classify_email(full_text, final_sender)

        return {
            "category": category,
            "response": response_text,
            "source": source,
            "sender": final_sender,
            "subject": final_subject,
            "text_length": len(full_text)
        }

    except Exception as e:
        logger.error(f"Erro na rota de classificação: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")