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
    libwoff2-1.0-2 \
    libvpx7 \
    libevent-2.1-7 \
    libopus0 \
    libgstallocators-1.0-0 \
    libgstapp-1.0-0 \
    libgstbase-1.0-0 \
    libgstpbutils-1.0-0 \
    libgstaudio-1.0-0 \
    libgsttag-1.0-0 \
    libgstvideo-1.0-0 \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libgstfft-1.0-0 \
    libflite1 \
    libflite1-plugins \
    libwebpdemux2 \
    libavif15 \
    libharfbuzz-icu0 \
    libwebpmux3 \
    libenchant-2-2 \
    libhyphen0 \
    libmanette-0.2-0 \
    libnghttp2-14 \
    libgles2 \
    libx264-164 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python3 -m playwright install

CMD ["bash", "start.sh"]

