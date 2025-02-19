# Use a minimal Python image
FROM python:3.10.12-slim

# Set the working directory
WORKDIR /app

# Set proxy environment variables (optional)
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY
ENV NO_PROXY=$NO_PROXY

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    cmake \
    make \
    pkg-config \
    libcairo2 \
    libcairo2-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    gobject-introspection \
    libsystemd-dev \
    swig \
    libssl-dev \
    libcups2-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
#RUN apt-get install apturl
# Upgrade pip, setuptools, and wheel to avoid legacy build issues
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy only essential files first (improves caching)
COPY requirements.txt .

# Ensure Python Packages and other dependencies install correctly
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port Streamlit will run on
EXPOSE 4200

# Run the Streamlit app
CMD ["streamlit", "run", "ncs4200_mpls_backbone_using_ansible_streamlit.py", "--server.port=4200", "--server.address=0.0.0.0"]
