# Use explicit image + force stable registry behavior
FROM python:3.10-slim

WORKDIR /app

# Improve SSL + network stability inside containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Flask default port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]