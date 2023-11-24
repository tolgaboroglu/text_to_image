# Use the official Python 3.9 base image
FROM python:3.9-slim

# Install wkhtmltopdf dependencies
RUN apt-get update \
    && apt-get install -y \
        xvfb \
        libfontconfig \
        libjpeg-turbo8 \
        libxrender1 \
        fontconfig \
        xfonts-base \
        xfonts-75dpi

# Download and install wkhtmltopdf
RUN apt-get install -y wget \
    && wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb \
    && apt-get -f install -y \
    && rm wkhtmltox_0.12.6-1.bionic_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the default command to run your FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
