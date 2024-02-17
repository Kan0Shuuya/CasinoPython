# Check if target system has docker
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: docker is not installed.' >&2
  exit 1
fi

# Check if required images are available
if ! docker images | grep -q "casino"; then
  echo 'Warning: casino image is not available. Building image...' >&2
  # Build image
  docker build -t casino .
fi

# Check if volume for persistence is available
if ! docker volume ls | grep -q "casino"; then
  echo 'Warning: casino volume is not available. Creating volume...' >&2
  # Create volume
  docker volume create casino
  # As the volume is empty, we need to create secrets.ini in it
  docker run -v casino:/persist --rm ubuntu:latest /bin/bash -c "echo [secrets]\nSECRET_KEY = \"$(openssl rand -base64 32)\" > /persist/secrets.ini"
fi

# Check if container is already running
if docker ps | grep -q "casino"; then
  echo 'Error: casino container is already running.' >&2
  exit 1
fi

# Run target image
docker run -d --restart unless-stopped --mount source=casino,target=/persist -p 25565:25565 casino
