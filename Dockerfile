FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y tar wget blender python3-pip 

RUN pip3 install poetry

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt && pip install -r requirements.txt

# RUN mkdir -p $HOME/.config/blender/3.0/scripts/addons
RUN wget -O blender-connector.zip https://releases.speckle.dev/installers/blender/bpy_speckle-2.17.0-alpha2.zip
RUN blender --background --python installation/connector.py 
