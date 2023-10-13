FROM linuxserver/blender

RUN apt update && \
    apt install python3-pip && \
    apt install unzip && \
    pip install poetry

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt && pip install -r requirements.txt

RUN curl -o blender-connector.zip https://github.com/specklesystems/speckle-blender/archive/refs/tags/2.16.0-rc1.zip && \
    unzip blender-connector.zip -d "$HOME/.config/blender/3.3/"
