FROM python:3.9.7-slim

LABEL maintainer="Your Name <your.email@example.com>" \
      version="1.0" \
      description="Description of your application"

# Install wkhtmltopdf and wkhtmltoimage dependencies
RUN apk update \
    && apk add --no-cache \
        xvfb \
        fontconfig \
        libjpeg-turbo \
        libxrender \
        xorg-server \
        ttf-dejavu \
        ttf-droid \
        ttf-freefont \
        ttf-liberation \
        ttf-ubuntu-font-family

# Download and install wkhtmltoimage
RUN apk add --no-cache wget \
    && wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.apk \
    && apk add --no-cache --allow-untrusted wkhtmltox_0.12.6-1.bionic_amd64.apk \
    && rm wkhtmltox_0.12.6-1.bionic_amd64.apk


RUN pip install --upgrade pip

WORKDIR /app

# Set the environment variable for wkhtmltoimage path
ENV WKHTMLTOIMAGE_PATH=/usr/local/bin/wkhtmltoimage

# Copy the requirements file and the current directory contents into the container at /app
COPY requirements.txt ./
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
