from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

APP_NAME = "student-ml-api"
VERSION_FILE = Path(__file__).with_name("VERSION")


def get_application_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


class PredictionRequest(BaseModel):
    value: float

    @field_validator("value", mode="before")
    @classmethod
    def value_must_be_numeric(cls, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("value must be numeric")
        return value


app = FastAPI(title=APP_NAME)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": APP_NAME,
        "version": get_application_version(),
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    return {
        "input": request.value,
        "prediction": request.value * 2,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=5000)
