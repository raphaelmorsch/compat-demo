FROM registry.access.redhat.com/ubi9/python-311:latest

WORKDIR /opt/app-root/src
COPY server.py .

# Instala ferramentas úteis de rede (UBI9/RHEL9)
# - iputils: ping
# - iproute: ip/ss/route
# - net-tools: netstat/ifconfig (legado, mas ainda útil)
# - bind-utils: dig/nslookup
# - nmap-ncat: nc
# - traceroute: traceroute
# - tcpdump: captura (pode exigir capabilities no Pod)
# - procps-ng: ps/top (às vezes ajuda no debug)
USER 0
RUN microdnf -y update && \
    microdnf -y install \
      iputils \
      iproute \
      net-tools \
      bind-utils \
      nmap-ncat \
      traceroute \
      tcpdump \
      procps-ng \
      && microdnf clean all && \
      rm -rf /var/cache/yum
USER 1001

ENV PORT=8080
EXPOSE 8080

CMD ["python", "server.py"]