FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir uvicorn fastapi

COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 8080

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
