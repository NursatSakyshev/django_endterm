# Use the official Python image as the base
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and to ensure stdout/stderr logs are shown
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /app

# Expose the port that the Django app runs on
EXPOSE 8000

# Run the Django development server (or replace with WSGI server for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
