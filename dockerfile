# Use the official Python image as the base image
FROM python:3.9-slim

# Install required dependencies
RUN apt-get update && \
    apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libx11-dev \
    libjpeg62-turbo \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

# Install a specific version of wkhtmltopdf
RUN apt-get update && \
    apt-get install -y wkhtmltopdf=0.12.6-1

# Set a global variable for the dynamic path to wkhtmltopdf
ENV WKHTMLTOPDF_PATH /usr/bin/wkhtmltopdf

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Create a working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/wkhtmltopdf/bin/wkhtmltoimage.exe

# Copy the rest of the application code
COPY . .

# Expose the port on which Uvicorn will run
EXPOSE 8000

# Set the entry point to run Uvicorn
CMD ["uvicorn", "your_script:app", "--host", "0.0.0.0", "--port", "8000"]