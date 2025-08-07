FROM python:3.12-slim

# Install Playwright and browser dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libgbm1 \
    libgtk-3-0 \
    libgtk-4-1 \
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
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgraphene-1.0-0 \
    libatomic1 \
    libxslt1.1 \
    libwoff1 \
    libwoff2-1.0-1 \
    libevent-2.1-7 \
    libopus0 \
    libflite1 \
    libwebpdemux2 \
    libavif12 \
    libwebpmux3 \
    libenchant-2-2 \
    libhyphen0 \
    libnghttp2-14 \
    libgles2-mesa \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

