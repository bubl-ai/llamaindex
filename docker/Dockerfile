# Use an official base image with Python and Conda
FROM continuumio/anaconda3:latest

# Install additional dependencies (git, vim)
# Minimize the amount of data stored in that particular docker layer
RUN apt-get update && \
    apt-get install -y git vim && \
    rm -rf /var/lib/apt/lists/*

# Installs with  Conda
RUN conda install -c conda-forge \
    numpy \
    spacy

# Installs with pip
RUN pip install \
    llama-index \
    llama-parse \
    llama-index-finetuning \
    sentence-transformers \
    newsapi-python \
    yfinance

# SSH for GitHub authentication
# keyscan is used to avoid manually veryfying Github hosts
RUN mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy the current directory contents into the container at /llamaindex-project
COPY . /llamaindex-project

# Set the working directory inside the container
WORKDIR /llamaindex-project
ENV WORKDIR=/llamaindex-project
ENV PERSIST_DIR=/llamaindex-project/persist_dir
ENV DATA_DIR=/llamaindex-project/data

# Install Python dependencies using pip
RUN pip install -e . --no-binary :all:

ENV WORKDIR=/llamaindex-project

# Specify the command to run on container startup
CMD ["/bin/bash"]