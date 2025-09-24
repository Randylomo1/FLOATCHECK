# Use a slim Python 3.11 base image
FROM python:3.11-slim

# Install dependencies for WeasyPrint
RUN apt-get update && apt-get install -y netcat-openbsd libpango-1.0-0 libpangoft2-1.0-0 libgobject-2.0-0 libffi-dev libcairo2 gdk-pixbuf2.0-0 shared-mime-info

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY mysite/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Define the entrypoint to run the Django development server
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
