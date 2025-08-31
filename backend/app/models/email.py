from pydantic import BaseModel
from typing import Optional

class EmailRequest(BaseModel):
    sender: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    file: Optional[str] = None
