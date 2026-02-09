FROM python:3.12-slim

# system tools (tcpdump, ping, etc.)
RUN apt-get update && apt-get install -y \
    tcpdump \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the project files
COPY . .

# default command
CMD ["tail", "-f", "/dev/null"]