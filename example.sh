#!bin/sh

script() {
    echo "Start" # String output

    # Receive variable by user input
    echo "Put your name"      # String output
    read name                 # Read input variable by user
    echo Your name is ${name} # Output input variable

    # Execute commands of another programs (like docker, git...)
    docker -v
    git --version

    # Insert rm Dockerfile and create again
    # putting first line in Dockerfile
    rm Dockerfile
    touch Dockerfile
    echo "FROM alpine:3.14" >>Dockerfile                                       # Input echo string inside file
    echo 'ENTRYPOINT ["echo", "Container running 👍 ( ͡° ͜ʖ ͡°)"]' >>Dockerfile # Input echo string inside file
    echo 'CMD ["'${name}'"] && /dev/null' >>Dockerfile                         # Input echo string inside file

    # Build and Execute Docker Container
    imageName="${name}-docker-image" # variable string
    docker build -t ${imageName} .   # build image
    docker images                    # list images

    # Generate utils variables
    timestamp=$(date +%s)                                 # variable string timestamp using date
    containerName="${name}-docker-container-${timestamp}" # variable string

    # Running command and see logs
    echo "-------"
    echo "Start: " && docker run -d --name ${containerName} ${imageName} # running container
    echo "-------"
    echo "Logs: " && docker logs ${containerName} # logs container
    echo "-------"
    # Remove all Containers
    containers=$(docker ps -a --format "{{.Names}}" | grep "${name}-docker-container") # list all containers created in this script
    docker rm -f ${containers}                                                         # remove all containers created in this script
    docker ps -a                                                                       # list all containers

    # Remove all Images
    imgs=$(docker images --format "{{.Repository}}" | grep "${imageName}")
    docker rmi -f ${imgs}
}

script | tee ex.log # fill log file called ex.log
