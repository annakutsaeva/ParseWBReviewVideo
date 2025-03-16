from pydantic import BaseModel


class HTMLData(BaseModel):
    html: str
