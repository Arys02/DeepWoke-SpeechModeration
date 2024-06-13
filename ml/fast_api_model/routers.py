from fastapi import APIRouter, HTTPException
from .schemas import TextItem
from .dependencies import predict_class

router = APIRouter()

