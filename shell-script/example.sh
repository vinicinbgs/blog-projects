#!bin/sh

script() {
    echo "Start" # Output Start in terminal

    # Receive variable by user input
    echo "Put your name"      # Output Put your name in terminal
    read name                 # Wait/Receive input variable name by user
    echo Your name is ${name} # Output Your name is variable name

    # Execute commands of another programs (like docker, git...)
    docker -v # docker version
    git --version # git version


    rm Dockerfile # Remove old Dockerfile
    touch Dockerfile # Create Dockerfile
    echo "FROM alpine:3.14" >>Dockerfile # Input echo string inside file
    echo 'ENTRYPOINT ["echo", "Container running 👍 ( ͡° ͜ʖ ͡°)"]' >>Dockerfile # Input echo string inside file
    echo 'CMD ["'${name}'"] && /dev/null' >>Dockerfile # Input echo string inside file

    # Build and Execute Docker Container
    imageName="${name}-docker-image" # docker image name variable
    docker build -t ${imageName} .   # build image
    docker images                    # list images

    # Generate utils variables
    timestamp=$(date +%s)                                 # create variable timestamp to attach in container name
    containerName="${name}-docker-container-${timestamp}" # variable container name to assign in run command

    # Running command and see logs
    echo "-------"
    echo "Start: " && docker run -d --name ${containerName} ${imageName} # running container
    echo "-------"
    echo "Logs: " && docker logs ${containerName} # output logs container
    echo "-------"
    
    # Remove all Containers
    containers=$(docker ps -a --format "{{.Names}}" | grep "${name}-docker-container") # list all containers created in this script
    docker rm -f ${containers}                                                         # remove all containers created in this script
    docker ps -a                                                                       # list all containers

    # Remove all Images
    imgs=$(docker images --format "{{.Repository}}" | grep "${imageName}") # imgs created repository
    docker rmi -f ${imgs} # Remove images in imgs variable
}

script | tee ex.log # fill log file called ex.log
