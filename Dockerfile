# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables (can be overridden at runtime)
ENV APP_VERSION=1.0
ENV APP_TITLE="Devops for Cloud Assignment"

# Run the application when the container launches
CMD ["uvicorn", "main:asgi_app", "--host", "0.0.0.0", "--port", "8000"]