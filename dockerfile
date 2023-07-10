# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code to the container
COPY . .

# Expose port 80 for the Flask application
EXPOSE 80

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask application on port 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
