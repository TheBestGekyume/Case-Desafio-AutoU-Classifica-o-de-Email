from fastapi import UploadFile, HTTPException
import logging
from PyPDF2 import PdfReader
import io

logger = logging.getLogger(__name__)

def extract_pdf_text(file: UploadFile) -> str:
    try:
        # Lê o conteúdo do arquivo
        file_content = file.file.read()
        
        # Verifica se o arquivo está vazio
        if len(file_content) == 0:
            return ""
            
        # Cria um leitor de PDF
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        
        # Extrai texto de cada página
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # Limita o texto extraído para evitar problemas de processamento
        if len(text) > 5000:
            text = text[:5000] + "... [texto truncado]"
            
        logger.info(f"Texto extraído do PDF: {len(text)} caracteres")
        return text
        
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")