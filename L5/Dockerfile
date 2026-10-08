FROM python:3.11-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY inventory_manager.py inventory.json ./

CMD ["python", "inventory_manager.py"]
