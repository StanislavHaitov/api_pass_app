# Use the official Python image with Alpine Linux
FROM python:3.8-alpine

# Update package lists and install curl
RUN apk update && apk add --no-cache curl

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY pass_app.py ./

# Specify the command to run your application
CMD ["python", "pass_app.py"]
