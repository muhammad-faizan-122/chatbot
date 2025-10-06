FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (for pip to work with scientific packages)
RUN apk add --no-cache \
    gcc musl-dev libffi-dev libstdc++ g++

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and MongoDB port
EXPOSE 8501
EXPOSE 27017

# Default command
CMD ["streamlit", "run", "app.py"]
