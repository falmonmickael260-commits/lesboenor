FROM python:3.13-slim
WORKDIR /app
COPY server.py questions.py ./
COPY public/ ./public/
CMD ["python","server.py"]
