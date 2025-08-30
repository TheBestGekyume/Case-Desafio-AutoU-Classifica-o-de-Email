from pydantic import BaseModel
from typing import Optional

class EmailRequest(BaseModel):
    sender: str
    subject: str
    message: str
    file_text: Optional[str] = None