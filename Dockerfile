# Use the tnk4on/yt-dlp image as the base
FROM tnk4on/yt-dlp

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY source ./source
COPY start.sh ./start.sh
COPY requirements.txt ./requirements.txt

# Install any additional Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Python script
# CMD ["python3", "source/main.py"]
CMD ["tail", "-f", "/dev/null"]
