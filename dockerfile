FROM python:3.9.7-slim

LABEL maintainer="Your Name <your.email@example.com>" \
      version="1.0" \
      description="Description of your application"

RUN apt-get update && \
    apt-get install -y \
        xvfb \
        libfontconfig \
        libjpeg-turbo8 \
        libxrender1 \
        fontconfig \
        xfonts-base \
        xfonts-75dpi \
        wget && \
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    apt-get -f install -y && \
    rm wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /app

# Copy the requirements file and the current directory contents into the container at /app
COPY requirements.txt ./
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
