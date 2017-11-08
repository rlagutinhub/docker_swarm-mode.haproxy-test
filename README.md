## Docker: docker_swarm-mode.haproxy-test

Compiled Docker image: https://hub.docker.com/r/rlagutinhub/docker_swarm-mode.haproxy-test/

-	The image is used to test the work docker_swarm-mode.haproxy-balancer reverse proxy in Docker Swarm Mode.
-	Base image python:3

#### Manual install

```console
git clone https://github.com/rlagutinhub/docker_swarm-mode.haproxy-test.git
cd docker_swarm-mode.haproxy-test
```

Docker Image:

```console
docker build -t rlagutinhub/docker_swarm-mode.haproxy-test:201711082130 .
```

Docker network:

```console
docker network create -d  overlay  haproxy-balancer_prod
```

Docker service:

```console
docker service create --detach=false \
 --name haproxy-test \
 -e PORTS="8080, 8081, 8082, 8083, 8084, 8085" \
 --network haproxy-balancer_prod \
 --constraint "node.role != manager" \
 rlagutinhub/docker_swarm-mode.haproxy-test:201711082130
```

Other:

#### ADD Publish Ports (not required for a haproxy-balancer test):

```console
docker service update --detach=false \
 haproxy-test \
 --publish-rm 80/tcp \
 --publish-add published=8080,target=8080,protocol=tcp \
 --publish-add published=8081,target=8081,protocol=tcp \
 --publish-add published=8082,target=8082,protocol=tcp \
 --publish-add published=8083,target=8083,protocol=tcp \
 --publish-add published=8084,target=8084,protocol=tcp \
 --publish-add published=8085,target=8085,protocol=tcp
```

#### RM Publish Ports (not required for a haproxy-balancer test):

```console
docker service update --detach=false \
 haproxy-test \
 --publish-rm 8080/tcp \
 --publish-rm 8081/tcp \
 --publish-rm 8082/tcp \
 --publish-rm 8083/tcp \
 --publish-rm 8084/tcp \
 --publish-rm 8085/tcp
 ```
