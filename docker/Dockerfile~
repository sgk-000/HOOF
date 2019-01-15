FROM ros:kinetic
MAINTAINER Koby
RUN apt update && apt install -y

RUN apt-get install emacs -y
RUN apt-get -y install bash-completion git build-essential emacs

WORKDIR /root/
RUN git clone https://github.com/orz-000/HOOF.git
#RUN git clone https://github.com/orz-000/video_stream_opencv.git
#RUN  mkdir -p ~/catkin_ws/src
#RUN /bin/bash -c 'source /opt/ros/kinetic/setup.bash; catkin_init_workspace ~/catkin_ws/src'

#RUN  mv HOOF/HOOF_ROS_pkg/ /root/catkin_ws/src/
#RUN  mv video_stream_opencv/ /root/catkin_ws/src/
RUN apt install -y ros-kinetic-cv-bridge
RUN apt install -y ros-kinetic-image-transport
RUN apt install -y ros-kinetic-camera-info-manager
RUN apt install -y ros-kinetic-image-view
#RUN  cd ~/catkin_ws/
#RUN  ["/bin/bash", "-c", "catkin_make"]

#RUN  apt-get install python-pip python-dev build-essential -y
#RUN pip install --upgrade pip
#RUN pip install opencv-python && pip install opencv-contrib-python
#RUN pip install scikit-video



