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
docker build -t rlagutinhub/docker_swarm-mode.haproxy-test:201711111920 .
```

Docker network:

```console
docker network create -d  overlay  haproxy-balancer_prod
```

Docker service:

```console
docker service create --detach=false \
 --name haproxy-test \
 -e PORTS="8080, 8081, 8443, 8444, 10001, 10002" \
 --network haproxy-balancer_prod \
 --constraint "node.role != manager" \
 rlagutinhub/docker_swarm-mode.haproxy-test:201711111920
```

#### ADD Publish Ports (not required for a haproxy-balancer test):

```console
docker service update --detach=false \
 haproxy-test \
 --publish-rm 80/tcp \
 --publish-add published=8080,target=8080,protocol=tcp \
 --publish-add published=8081,target=8081,protocol=tcp \
 --publish-add published=8443,target=8443,protocol=tcp \
 --publish-add published=8444,target=8444,protocol=tcp \
 --publish-add published=10001,target=10001,protocol=tcp \
 --publish-add published=10002,target=10002,protocol=tcp
```

#### RM Publish Ports (not required for a haproxy-balancer test):

```console
docker service update --detach=false \
 haproxy-test \
 --publish-rm 8080/tcp \
 --publish-rm 8081/tcp \
 --publish-rm 8443/tcp \
 --publish-rm 8444/tcp \
 --publish-rm 10001/tcp \
 --publish-rm 10002/tcp
 ```
  
---

![alt text](https://github.com/rlagutinhub/docker_swarm-mode.haproxy-test/blob/master/screen.png)
