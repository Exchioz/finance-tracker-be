from pydantic import BaseModel
from typing import Any, Optional

class StandardResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None