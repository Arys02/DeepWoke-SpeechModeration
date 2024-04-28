from pydantic import BaseModel


class TextItem(BaseModel):
    text: str
    is_hate_speech: bool

    class Config:
        schema_extra = {
            "example": {
                "text": "Sample input text"
            }
        }