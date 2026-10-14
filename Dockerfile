# Use an official, lightweight Python base environment image
FROM python:3.12-slim

# Set environment system performance configurations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establish our tracking workspace directory inside the container unit
WORKDIR /app

# Install system dependencies needed for compiling certain packages
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc-dev && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies checklist
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files over
COPY . /app/

# Run static asset gathering routines automatically during image construction
RUN python manage.py collectstatic --noinput

# Expose network tracking port 8000
EXPOSE 8000

# Launch the application using a production WSGI HTTP server wrapper
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "partyStore.wsgi:application"]
