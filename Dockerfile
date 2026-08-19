# Use the slim Python 3.12 image as the base for this website container.
# This provides the Python runtime required by the Flask site while keeping the image relatively small.
FROM python:3.12-slim

# Set /app as the working directory inside the container.
# Relative paths used by later COPY, RUN, and CMD instructions are resolved from here.
WORKDIR /app

# Copy requirements.txt into the current working directory inside the container.
# Keeping this step separate allows Docker to reuse the dependency-install layer when only source files change.
COPY requirements.txt .

# Install the Python packages required by the website.
# --no-cache-dir prevents pip from keeping its package cache and helps reduce the final image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project directory into /app inside the container.
# This brings app.py, templates, static assets, routes, services, and database modules into the runtime image.
COPY . .

# Document that the website process inside the container listens on port 3000.
# External access still depends on the port mapping configured in docker-compose.
EXPOSE 3000

# Start the Flask site with gunicorn when the container launches.
# gunicorn is a production-oriented WSGI server and is more suitable for deployment than running python app.py directly.
# --bind 0.0.0.0:3000 makes the site listen on every container network interface at port 3000.
# --workers 1 keeps the current deployment on a single worker so the embedded scheduler is not started multiple times.
# app:app means: load the Flask application object named app from app.py.
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "1", "app:app"]
