FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV BLENDER_VERSION=3.0.1
RUN \
  echo "**** install packages ****" && \
  apt-get update && \
  apt-get install --no-install-recommends -y \
  libopenexr-dev \ 
  bzip2 \ 
  build-essential \ 
  zlib1g-dev \ 
  libxmu-dev \ 
  libxi-dev \ 
  libxkbcommon-x11-0 \
  libxxf86vm-dev \ 
  libfontconfig1 \ 
  libxrender1 \ 
  libgl1-mesa-glx \ 
  wget \
  curl \
  python3-pip \
  ocl-icd-libopencl1 \
  xz-utils
  
RUN \
  ln -s libOpenCL.so.1 /usr/lib/x86_64-linux-gnu/libOpenCL.so && \
  echo "**** install blender ****" && \
  mkdir /blender && \
  if [ -z ${BLENDER_VERSION+x} ]; then \
  BLENDER_VERSION=$(curl -sL https://mirrors.ocf.berkeley.edu/blender/source/ \
  | awk -F'"|/"' '/blender-[0-9]*\.[0-9]*\.[0-9]*\.tar\.xz/ && !/md5sum/ {print $4}' \
  | tail -1 \
  | sed 's|blender-||' \
  | sed 's|\.tar\.xz||'); \
  fi && \
  BLENDER_FOLDER=$(echo "Blender${BLENDER_VERSION}" | sed -r 's|(Blender[0-9]*\.[0-9]*)\.[0-9]*|\1|') && \
  curl -o \
  /tmp/blender.tar.xz -L \
  "https://mirrors.ocf.berkeley.edu/blender/release/${BLENDER_FOLDER}/blender-${BLENDER_VERSION}-linux-x64.tar.xz" && \
  tar xf \
  /tmp/blender.tar.xz -C \
  /blender/ --strip-components=1 && \
  ln -s \
  /blender/blender \
  /usr/bin/blender && \
  echo "**** cleanup ****" && \
  rm -rf \
  /tmp/* \
  /var/lib/apt/lists/* \
  /var/tmp/*

RUN pip3 install poetry


COPY . .

RUN poetry export -f requirements.txt --output requirements.txt && pip install -r requirements.txt && \
  wget -O blender-connector.zip https://releases.speckle.dev/installers/blender/bpy_speckle-2.17.0.zip && \
  blender --background --python installation/connector.py 