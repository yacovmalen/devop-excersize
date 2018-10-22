docker build -t devop-exercize -f deployment/Dockerfile .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v /public/images:/public/images --net=host devop-exercize