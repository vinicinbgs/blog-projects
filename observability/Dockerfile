# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./app.py ./app.py
COPY ./loggingz ./loggingz
COPY ./logging.json ./logging.json

# Expose port 9999 for the Flask application
EXPOSE 9999

# Run the application
CMD ["python", "app.py"]