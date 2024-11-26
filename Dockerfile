# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Set environment variables (can be overridden in deployment)
ENV PYTHONUNBUFFERED=1

# Expose the port (optional, not mandatory for bots)
EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
