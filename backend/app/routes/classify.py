from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging
from app.services.classify_service import classify_email
from app.services.pdf_service import extract_pdf_text

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/classify")
async def classify_email_route(
    subject: str = Form(...),
    message: str = Form(...),
    sender: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        # Extrai texto do PDF se anexado
        file_text = ""
        if file and file.filename and file.filename.lower().endswith('.pdf'):
            file_text = await extract_pdf_text(file)
        
        # Combina todo o texto para classificação
        full_text = f"Assunto: {subject}\nMensagem: {message}"
        if file_text:
            full_text += f"\n\nConteúdo do Anexo: {file_text}"
            
        logger.info(f"Texto para classificação: {len(full_text)} caracteres")
        logger.info(f"Remetente: {sender}")
           
        # Classifica usando o serviço
        category, response_text, source = classify_email(full_text, sender)

        return {
            "category": category,
            "response": response_text,
            "source": source,
            "sender": sender,
            "text_length": len(full_text)
        }

    except Exception as e:
        logger.error(f"Erro na rota de classificação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")