
FROM python:3.10-slim

WORKDIR /app

COPY ./backend /app/backend
COPY ./models /app/models

RUN pip install langchain openai llama-cpp-python fastapi uvicorn

CMD ["uvicorn", "backend.main_api:app", "--host", "0.0.0.0", "--port", "8000"]
