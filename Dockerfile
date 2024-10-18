# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies including git and openssh-client
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/sddiener/CaveScraperApp.git .

# Copy the rest of the application code to the working directory
COPY . .

# Run the requirements.txt file from the working directory
RUN pip3 install -r requirements.txt

# Health Check instruction tells Docker how to test a container to check that it is still working
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Expose the port Streamlit runs on
EXPOSE 8501

# Configure a container that will run as an executable
# also contains the entire streamlit run command for your app, so you don’t have to call it from the command line
# alternatively have your CMD command run the streamlit run command
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
