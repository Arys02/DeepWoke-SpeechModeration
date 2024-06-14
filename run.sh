#!/bin/bash
uvicorn ml.fast_api_model.main:app --host 0.0.0.0 --port ${PORT:-8000}
