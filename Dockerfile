FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libgbm1 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatspi2.0-0 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libx11-xcb1 \
    fonts-liberation \
    libappindicator3-1 \
    libsecret-1-0 \
    lsb-release \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python3 -m playwright install

CMD ["bash", "start.sh"]
