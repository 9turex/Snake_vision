FROM python

WORKDIR /python_vision_docker

COPY . .

RUN pip uninstall PyQt5 \
    && pip install opencv-python \
    && apt-get update \
    && apt-get install ffmpeg libsm6 libxext6

CMD ["python", "main.py"]
