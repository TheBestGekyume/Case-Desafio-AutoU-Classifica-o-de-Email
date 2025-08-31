import io
import re
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

async def extract_file_content(file: UploadFile) -> tuple[str, str, str, str]:
   
    try:
        filename = file.filename.lower()
        content = await file.read()

        if len(content) == 0:
            return "", None, None, None

        full_text = ""
        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
        elif filename.endswith(".txt"):
            full_text = content.decode("utf-8", errors="ignore")
        else:
            raise HTTPException(400, "Apenas arquivos PDF ou TXT são permitidos")

        sender = extract_sender(full_text)
        subject = extract_subject(full_text)
        message = extract_message(full_text)

        logger.info(f"Extraído do arquivo - Remetente: {sender}, Assunto: {subject}")

        return full_text, sender, subject, message

    except Exception as e:
        logger.error(f"Erro ao extrair arquivo: {str(e)}")
        raise HTTPException(500, f"Erro ao processar arquivo: {str(e)}")

def extract_sender(text: str) -> str:
    patterns = [
        r'Remetente:\s*(.+)',
        r'From:\s*(.+)',
        r'De:\s*(.+)',
        r'Sender:\s*(.+)',
        r'Enviado por:\s*(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None




def extract_subject(text: str) -> str:
    """Extrai o assunto do texto usando padrões comuns"""
    patterns = [
        r'Assunto:\s*(.+?)(?=\n\w+:|$)',
        r'Subject:\s*(.+?)(?=\n\w+:|$)',
        r'Título:\s*(.+?)(?=\n\w+:|$)',
        r'Title:\s*(.+?)(?=\n\w+:|$)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            subject = match.group(1).strip()
            subject = re.sub(r'\s+', ' ', subject)
            return subject
    
    subject_match = re.search(r'Assunto:\s*(.+?)(?=\n\s*\n|\n\w+:|$)', text, re.IGNORECASE | re.DOTALL)
    if subject_match:
        subject = subject_match.group(1).strip()
        subject = re.sub(r'\s+', ' ', subject)
        return subject
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line and len(line) < 100 and not line.lower().startswith(('remetente', 'from', 'de', 'sender')):
            if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith(('Mensagem', 'Message')):
                return f"{line} {lines[i + 1].strip()}"
            return line
    
    return None


def extract_message(text: str) -> str:
    lines = text.split('\n')
    message_lines = []
    in_message = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if re.match(r'(Mensagem|Message|Corpo|Body):', line, re.IGNORECASE):
            in_message = True
            continue
            
        if in_message and re.match(r'(Remetente|From|De|Sender|Assunto|Subject):', line, re.IGNORECASE):
            break
            
        if in_message or not re.match(r'(.+):\s*.+', line): 
            message_lines.append(line)
    
    message = ' '.join(message_lines)
    
    if not message.strip():
        return text
    
    return message