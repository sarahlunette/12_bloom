from datetime import datetime

from pydantic import BaseModel

from typing import Union


class PipelineRun(BaseModel):
    id: Union[ int , None ] = None
    timestamp: datetime
    code: str
    session: str
