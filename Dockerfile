FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TRANSFORMERS_CACHE=/models/hf_cache
ENV HF_HOME=/models/hf_cache

# System dependencies
RUN apt-get update && apt-get install -y python3-pip git && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --upgrade pip

WORKDIR /app

# Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Model files and license
COPY ./tinyllama-model /models/tinyllama
COPY LICENSE /models/tinyllama/LICENSE

# Application file
COPY main.py ./

# Port
EXPOSE 5555

# Run the application
CMD ["python3", "-u", "main.py"]
