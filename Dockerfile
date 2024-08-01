# Use the base image with yt-dlp pre-installed
FROM tnk4on/yt-dlp:latest

USER root

# Set the working directory in the container
WORKDIR /app

# Install Python 3 and pip
RUN apk add --no-cache python3 py3-pip

# Copy your Python script into the container
COPY . .

# Install any required Python packages
# If you have a requirements.txt file, uncomment the following lines:
RUN pip3 install --no-cache -r requirements.txt
RUN yt-dlp -U
RUN mkdir videos

ENTRYPOINT ["/usr/bin/env"]

# Set the default command to run your Python script
CMD ["python3", "source/main.py"]
