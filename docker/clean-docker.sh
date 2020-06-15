# /bin/bash

docker rm $(docker ps -q --filter status=exited --filter status=created)

docker rmi $(docker images --quiet --filter "dangling=true")

docker volume rm $(docker volume ls -q)

# docker system df
