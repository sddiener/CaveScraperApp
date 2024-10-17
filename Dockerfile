# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables using the preferred format
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wkhtmltopdf git openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

# Install Python dependencies using SSH forwarding
RUN --mount=type=ssh pip install --upgrade pip && \
    pip install -r requirements.txt


# Copy project files
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
