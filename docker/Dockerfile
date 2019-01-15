FROM ros:kinetic
MAINTAINER Koby
RUN apt update && apt install -y

RUN apt-get install emacs -y
RUN apt-get -y install bash-completion git build-essential emacs

WORKDIR /root/
RUN git clone https://github.com/orz-000/HOOF.git
RUN apt install -y ros-kinetic-cv-bridge
RUN apt install -y ros-kinetic-image-transport
RUN apt install -y ros-kinetic-camera-info-manager
RUN apt install -y ros-kinetic-image-view
