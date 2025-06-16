FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /backend/src

WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir -r /backend/requirements.txt

COPY src /backend/app
COPY main.py /backend/main.py
COPY config.py /backend/src/presentation/config.py

LABEL org.opencontainers.image.source=https://github.com/Grupo-ASD/NOMBRE-REPOSITORIO

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

USER appuser

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]