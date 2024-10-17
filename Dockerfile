# syntax=docker/dockerfile:1.4

# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files and to ensure stdout and stderr are unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including git and openssh-client
RUN apt-get update && \
    apt-get install -y wkhtmltopdf git openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Add GitHub to known_hosts to prevent host verification prompts
RUN mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install Python dependencies using SSH forwarding
RUN --mount=type=ssh pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Define the default command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
