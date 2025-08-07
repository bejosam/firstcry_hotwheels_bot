FROM python:3.12-slim

# Install system dependencies for Playwright browsers
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libxkbcommon0 \
    libx11-6 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libdrm2 \
    fonts-liberation \
    libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt && playwright install

CMD ["python3", "hotwheels_bot.py"]

