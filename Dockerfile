FROM python:3.13.3-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install the package
COPY package ./package

RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install --no-cache-dir -e ./package --root-user-action=ignore

RUN pip install kagglehub==0.3.12 --root-user-action=ignore
RUN pip install flask==3.1.1 --root-user-action=ignore
RUN pip install gunicorn==23.0.0 --root-user-action=ignore

# Copy your code
COPY UI ./UI
COPY wsgi.py .

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
