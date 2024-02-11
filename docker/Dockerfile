# Use an official myenv image with Python and Conda
FROM continuumio/anaconda3:latest

# Install additional dependencies (git, vim)
# Minimise the amount of data stored in that particular docker layer (rm -rf /var/lib/apt/lists/*)
RUN apt-get update && \
    apt-get install -y git vim && \
    rm -rf /var/lib/apt/lists/*  

# Create and activate a Conda environment
RUN conda create --name myenv python=3.8 && \
    echo "conda activate myenv" >> ~/.bashrc

# Install numpy in the Conda environment
RUN conda install -n myenv numpy

# Copy the current directory contents into the container at /llamaindex-project
COPY . /llamaindex-project

# Install Python dependencies using pip
RUN pip install -e . --no-binary :all:

# Set the working directory inside the container
WORKDIR /llamaindex-project

# Specify the command to run on container startup
CMD ["/bin/bash"]