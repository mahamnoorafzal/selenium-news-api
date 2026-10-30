
FROM python:3.12-slim

# Install Chrome browser and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY scraper.py .
COPY summarizer.py .

# Expose API port
EXPOSE 7000

# Start Flask API automatically
CMD ["python", "app.py"]
