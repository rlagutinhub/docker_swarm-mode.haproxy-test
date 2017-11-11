# vendor="Lagutin R.A."
# maintainer="Lagutin R.A. <rlagutin@mta4.ru>"
# name="docker_swarm-mode.haproxy-test"
# description="docker_swarm-mode.haproxy-test"
# version="v.3-prod."
# release-date="201711111920"

# Build Image:
# docker build -t rlagutinhub/docker_swarm-mode.haproxy-test:201711111920 .

# Network:
# docker network create -d  overlay  haproxy-balancer_prod

# Create service:
# docker service create --detach=false \
#  --name haproxy-test \
#  -e PORTS="8080, 8081, 8443, 8444, 10001, 10002" \
#  --network haproxy-balancer_prod \
#  --constraint "node.role != manager" \
#  rlagutinhub/docker_swarm-mode.haproxy-test:201711111920

# ADD Publish Ports (not required for a haproxy-balancer test):
#docker service update --detach=false \
# haproxy-test \
# --publish-rm 80/tcp \
# --publish-add published=8080,target=8080,protocol=tcp \
# --publish-add published=8081,target=8081,protocol=tcp \
# --publish-add published=8443,target=8443,protocol=tcp \
# --publish-add published=8444,target=8444,protocol=tcp \
# --publish-add published=10001,target=10001,protocol=tcp \
# --publish-add published=10002,target=10002,protocol=tcp

# RM Publish Ports (not required for a haproxy-balancer test):
#docker service update --detach=false \
# haproxy-test \
# --publish-rm 8080/tcp \
# --publish-rm 8081/tcp \
# --publish-rm 8443/tcp \
# --publish-rm 8444/tcp \
# --publish-rm 10001/tcp \
# --publish-rm 10002/tcp

FROM python:3

LABEL rlagutinhub.community.vendor="Lagutin R.A." \
 rlagutinhub.community.maintainer="Lagutin R.A. <rlagutin@mta4.ru>" \
 rlagutinhub.community.name="docker_swarm-mode.haproxy-test" \
 rlagutinhub.community.description="docker_swarm-mode.haproxy-test" \
 rlagutinhub.community.version="v.3-prod." \
 rlagutinhub.community.release-date="201711111920"

COPY app /app
WORKDIR /app

RUN chmod +x *.sh *.py && pip3 install -U -r requirements.txt

CMD ["./run.sh"]
