# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Go
ENV GO_VERSION 1.18.1
RUN curl -OL https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz \
    && rm go${GO_VERSION}.linux-amd64.tar.gz
ENV PATH $PATH:/usr/local/go/bin

# Install nmap and git (git is required to clone gobuster)
RUN apt-get update && apt-get install -y \
    nmap \
    git

# Install gobuster
RUN go install github.com/OJ/gobuster/v3@latest

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Copy your dictionary file into the container
COPY path/to/your/dictionary.txt /usr/src/app/dictionary.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "./main.py"]