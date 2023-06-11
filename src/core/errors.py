from typing import Dict, Union

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: Union[str, Dict[str, str]]
