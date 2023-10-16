FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install --no-install-recommends -y tar wget blender python3-pip && \
	pip3 install poetry

COPY . .

RUN poetry export -f requirements.txt --output requirements.txt && pip install -r requirements.txt && \
	wget -O blender-connector.zip https://releases.speckle.dev/installers/blender/bpy_speckle-2.17.0-alpha2.zip && \
	blender --background --python installation/connector.py 
