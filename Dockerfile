# Use a slim base image for a smaller final image
FROM python:3.10-slim as base

WORKDIR /app

# Install build dependencies if needed (optional multi-stage build)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
