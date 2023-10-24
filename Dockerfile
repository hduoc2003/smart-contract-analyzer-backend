# Stage 1: Build Python application
FROM python:3.10 AS builder

# Install uWSGI
RUN pip install uwsgi

# Set the working directory
WORKDIR /app

# Copy the application code
COPY ./app /app

# Install Python application dependencies
RUN pip install -r ./app/requirements.txt


# Stage 2: Build the final image with Nginx
FROM nginx

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the Nginx configuration file
COPY ./nginx/nginx.conf /etc/nginx/conf.d/
# Define the command to start Nginx

COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh
# Define the command to start your application using the entrypoint script
CMD ["/entrypoint.sh"]



# Expose port 8080 (if needed)
EXPOSE 80
# Stage 3: Set environment variables
ENV ENVIRONMENT production
ENV DATABASE_NAME TOOL-TEST
ENV MONGO_CONNECTION_STRING mongodb+srv://shodydosh:dT8NJQfeB25rAtj@cluster0.l96vywb.mongodb.net/
