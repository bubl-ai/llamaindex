For a more detailed description of this visit
[bubl-ai.com](https://bubl-ai.com/posts/Simple-Dockerfile-for-Dev-Purposes/)

# Use of Docker in AI

Dockerfiles, images, and containers are essential players in the realm of Artificial Intelligence development, creating a foundation for consistency and reproducibility. They shape a standardized environment for ML applications, ensuring uniformity in software dependencies, libraries, and configurations. This streamlines collaboration among data scientists, engineers, and stakeholders by mitigating challenges related to environment variations and dependency conflicts. Dockerized AI environments also bolster portability, facilitating the sharing and deployment of models across diverse computing environments, from local workstations to cloud infrastructure. This promotes efficient collaboration and deployment practices in the dynamic field of machine learning.

## A Simple Dockerfile Template for Your ML Projects

Here's a straightforward Dockerfile template that suits the requirements for the development of AI projects:

- Utilizes a base image with pre-installed Python and Conda.
- Installs basic dependencies.
- Sets up a Conda environment and installs all required libraries.
- Enables seamless GitHub authentication for source control within the container.
- Uses "pip install -e ." to install the current directory as a package, allowing users to treat their utilities within the container like any other library. This is discussed in more detail [here](https://bubl-ai.com/posts/Repo-as-Importable-Package/).

The next Dockerfile was gotten from our [*llamaindex-project repository.*](https://github.com/bubl-ai/llamaindex-project/blob/main/docker)

```
# Use an official base image with Python and Conda
FROM continuumio/anaconda3:latest

# Install additional dependencies (git, vim)
# Minimize the amount of data stored in that particular docker layer
RUN apt-get update && \
    apt-get install -y git vim && \
    rm -rf /var/lib/apt/lists/*

# Installs with  Conda
RUN conda install numpy

# Installs with pip
RUN pip install llama-index

# SSH for GitHub authentication
# keyscan is used to avoid manually veryfying GitHub hosts
RUN mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy the current directory contents into the container at /llamaindex-project
COPY . /llamaindex-project

# Set the working directory inside the container
WORKDIR /llamaindex-project

# Install Python dependencies using pip
RUN pip install -e . --no-binary :all:

# Specify the command to run on container startup
CMD ["/bin/bash"]
```

You can use it in VSCode to seamlessly develop your code within the container.
This is assuming that you already have Docker and VSCode installed, and that you set your GitHub ssh key in `~/.ssh/id_ed25519`. If you don't have this, feel free to check [this previous blog post](https://bubl-ai.com/posts/Raspberry-Pi-Setup/) and jump to the GitHub section.

The only thing missing is to build your image and run your container. This is done very easily by executing the next commands.
```bash
docker build -t [NAME_OF_IMAGE] -f Dockerfile .
docker run -t -d -v [PATH_TO_GITHUB_SSH_KEY]:/root/.ssh/id_ed25519 [NAME_OF_IMAGE] /bin/bash
```

## Security Tips for Docker

In the ever-evolving landscape of machine learning, ensuring a secure and adaptable Docker environment is crucial for the success of your projects.

Did you notice that we executed `docker run` with a volume to include the ssh key? Let us explain why. When it comes to security in Docker, especially handling sensitive information like SSH private keys, caution is key. Embedding such data directly into Docker images may pose security risks, particularly if shared or made public. Best practices recommend avoiding direct embedding of sensitive information into images.

Using a volume to provide sensitive information, such as an SSH key, during runtime is a more secure approach compared to embedding it in the Docker image. Here are the advantages:

- **Avoiding Image Exposure:** By not embedding sensitive information directly, the risk of unintentional exposure is reduced, especially in shared or public images.

- **Separation of Concerns:** Storing sensitive information in a volume allows for the separation of building the image and providing runtime configurations, enhancing security and maintainability.

- **Dynamic Configuration:** With a volume, sensitive information can be changed without rebuilding the Docker image. This flexibility is valuable when updating credentials or keys without redeploying the entire application.

> There seems to be a way to allow VSCode to automatically share the GitHub SSH key with your container. I haven't been able to make it work, but it is worth sharing, [LINK](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials). Let me know if it worked for you!

## Environmental Variables
Setting up environmental variables correctly is important for both the security and functionality of your images. Make sure you create them either in the command line while starting container with `docker run -e [ENV_VAR_NAME]=$ENV_VAR_NAME`, or inside the container by executing `export [ENV_VAR_NAME]=[VALUE]`. If you choose the former make sure to not pass the sensitive information directly on the command line.