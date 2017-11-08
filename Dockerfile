# vendor="Lagutin R.A."
# maintainer="Lagutin R.A. <rlagutin@mta4.ru>"
# name="docker_swarm-mode.haproxy-test"
# description="docker_swarm-mode.haproxy-test"
# version="v.1-prod."
# release-date="201711082130"

# Build Image:
# docker build -t rlagutinhub/docker_swarm-mode.haproxy-test .

# Network:
# docker network create -d  overlay  haproxy-balancer_prod

# Create service:
# docker service create --detach=false \
#  --name haproxy-test \
#  -e PORTS="8080, 8081, 8082, 8083, 8084, 8085" \
#  --network haproxy-balancer_prod \
#  --constraint "node.role != manager" \
#  rlagutinhub/docker_swarm-mode.haproxy-test:latest

# ADD Publish Ports (not required for a haproxy-balancer test):
#docker service update --detach=false \
# haproxy-test \
# --publish-rm 80/tcp \
# --publish-add published=8080,target=8080,protocol=tcp \
# --publish-add published=8081,target=8081,protocol=tcp \
# --publish-add published=8082,target=8082,protocol=tcp \
# --publish-add published=8083,target=8083,protocol=tcp \
# --publish-add published=8084,target=8084,protocol=tcp \
# --publish-add published=8085,target=8085,protocol=tcp

# RM Publish Ports (not required for a haproxy-balancer test):
#docker service update --detach=false \
# haproxy-test \
# --publish-rm 8080/tcp \
# --publish-rm 8081/tcp \
# --publish-rm 8082/tcp \
# --publish-rm 8083/tcp \
# --publish-rm 8084/tcp \
# --publish-rm 8085/tcp

FROM python:3

LABEL rlagutinhub.community.vendor="Lagutin R.A." \
 rlagutinhub.community.maintainer="Lagutin R.A. <rlagutin@mta4.ru>" \
 rlagutinhub.community.name="docker_swarm-mode.haproxy-test" \
 rlagutinhub.community.description="docker_swarm-mode.haproxy-test" \
 rlagutinhub.community.version="v.1-prod." \
 rlagutinhub.community.release-date="201711082130"

COPY app /app
WORKDIR /app

RUN chmod +x *.sh *.py && pip3 install -U -r requirements.txt

CMD ["./run.sh"]
