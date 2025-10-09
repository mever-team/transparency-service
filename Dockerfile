FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package ./package
COPY ui ./ui
# COPY endpoint/test_server.py .

RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install --no-cache-dir -e ./package --root-user-action=ignore
RUN pip install kagglehub==0.3.12 --root-user-action=ignore
RUN pip install flask==3.1.1 --root-user-action=ignore
RUN pip install gunicorn==23.0.0 --root-user-action=ignore

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "1", "--threads", "1", "--capture-output", "--log-level", "error", "--access-logfile", "-", "--error-logfile", "-", "ui.full_server:app"]
