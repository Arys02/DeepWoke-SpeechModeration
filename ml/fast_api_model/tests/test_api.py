from httpx import AsyncClient, ASGITransport
import pytest
from ml.fast_api_model.main import app  # Adjust the import according to your project structure


@pytest.mark.asyncio
async def test_prediction():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/classify/", json={"text": "example text"})

    assert response.status_code == 200
    assert response.json() == {"prediction": "we don't have a model yet"}
