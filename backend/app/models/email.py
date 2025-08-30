from pydantic import BaseModel
from typing import Optional

class EmailRequest(BaseModel):
    subject: str
    message: str
    file_text: Optional[str] = None