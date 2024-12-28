# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port (if using webhooks; optional)
EXPOSE 5000

# Run the application
CMD ["python", "src/main.py"]
