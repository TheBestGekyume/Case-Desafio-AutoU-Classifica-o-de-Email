from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging
from app.services.classify_service import classify_email
from ..services.file_service import extract_file_content

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/classify")
async def classify_email_route(
    sender: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        # Extrai conteúdo de arquivo se houver
        file_text = ""
        if file and file.filename:
            file_text, extracted_sender, extracted_subject, extracted_message = await extract_file_content(file)
            sender = sender or extracted_sender
            subject = subject or extracted_subject
            message = message or extracted_message
            file_text = file_text

        # Valida entrada
        if not file_text and (not subject or not message):
            raise HTTPException(
                status_code=400,
                detail="Envie um arquivo ou preencha subject e message."
            )

        # Monta o texto final
        full_text = file_text if file_text else f"Remetente: {sender}\nAssunto: {subject}\nMensagem: {message}"

        # Chama serviço centralizado
        category, response_text, source = classify_email(full_text, sender)

        return {
            "category": category,
            "response": response_text,
            "source": source,
            "sender": sender,
            "subject": subject,
            "text_length": len(full_text)
        }

    except Exception as e:
        logger.error(f"Erro na rota de classificação: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
