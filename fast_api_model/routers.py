from fastapi import APIRouter, HTTPException
from .schemas import TextItem
from .dependencies import predict_class

router = APIRouter()


@router.post("/classify/", response_model=dict[str, str])
async def classify_text(item: TextItem):
    classification = predict_class(item.text)
    if classification is None:
        raise HTTPException(status_code=404, detail="Classification failed")
    return {"class": classification}
