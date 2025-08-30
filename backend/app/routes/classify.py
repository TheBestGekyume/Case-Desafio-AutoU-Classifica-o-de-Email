from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging
from app.services.ai_service import classify_email
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
        file_text = ""
        
        if file and file.filename.endswith('.pdf'):
            file_text = extract_pdf_text(file)
        
        if file_text:
            full_text = f"\n\nConteúdo do Anexo: {file_text}"
        else:
            full_text = f"\n\nAssunto: {subject}\n\nMensagem: {message}"
            
        logger.info(f"Texto para classificação: {len(full_text)} caracteres")
           
        category, response_text, source = classify_email(full_text, sender)

        return {
            "category": category,
            "response": response_text,
            "source": source
        }


    except Exception as e:
        logger.error(f"Erro na rota de classificação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")