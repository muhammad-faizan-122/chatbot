FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (for pip to work with scientific packages)
RUN apk add --no-cache \
    gcc musl-dev libffi-dev libstdc++ g++

# copy requirements file from host machine current directory to container /app directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and MongoDB port
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]