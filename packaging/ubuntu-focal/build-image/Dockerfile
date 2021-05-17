FROM alanfranz/fpm-within-docker:ubuntu-focal
MAINTAINER Alan Franzoni <username@franzoni.eu>
ENV TZ Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive 
# whatever is required for building should be installed in this image; just like BuildDeps for DEB projects.
RUN apt-get update ; apt-get -y install rsync cmake libpcre3-dev python3
