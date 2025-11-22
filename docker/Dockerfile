FROM python:3.11
WORKDIR /app
COPY . /app

# Install system dependencies and Chromium (works on amd64 and arm64)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     wget curl ca-certificates gnupg \
#     fonts-liberation \
#     libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 \
#     libcairo2 libcups2 libcurl4 libdbus-1-3 libexpat1 libgbm1 \
#     libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libxss1 libpango-1.0-0 \
#     libudev1 libvulkan1 libx11-6 libxcb1 libxcomposite1 libxdamage1 \
#     libxext6 libxfixes3 libxkbcommon0 libxrandr2 \
#     chromium \
#  && rm -rf /var/lib/apt/lists/*

# # Ensure binary locations are known to the app
# ENV CHROME_BIN=/usr/bin/chromium
# ENV CHROMEDRIVER_PATH=/root/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver

# # Provide a google-chrome compatible symlink for tools expecting google-chrome
# # RUN ln -sf /usr/bin/chromium /usr/bin/google-chrome || true
# RUN apt-get update && apt-get install -y wget unzip \
#  && wget https://storage.googleapis.com/chrome-for-testing-public/142.0.7444.59/linux64/chromedriver-linux64.zip \
#  && unzip chromedriver-linux64.zip \
#  && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
#  && chmod +x /usr/bin/chromedriver


RUN pip install --upgrade pip
RUN rm -rf ~/.wdm/drivers
RUN pip install -r lib/requirements.txt