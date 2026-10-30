FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY main.py product.py inventory.py file_handling.py inventory.json ./

CMD ["python", "main.py"]
