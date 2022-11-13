FROM ubuntu:22.04

WORKDIR /opt/sudoku-solver
ADD . /opt/sudoku-solver

# update APT repos and apply patches
RUN apt-get update \
    && apt-get install -y software-properties-common gcc \
    && add-apt-repository -y ppa:deadsnakes/ppa

# python
RUN apt-get install -y python3-distutils python3-pip python3-dev

# tesseract
RUN add-apt-repository -y ppa:alex-p/tesseract-ocr5 \
    && apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
ENV TESSDATA_PREFIX /usr/share/tesseract-ocr/5/tessdata

# install cv2 dependencies
RUN apt-get install -y ffmpeg libsm6 libxext6

# requirements
RUN  pip3 install -r /opt/sudoku-solver/requirements.txt

# permissions
RUN chmod +x /opt/sudoku-solver/app/run.sh

EXPOSE 8001

CMD ["bash", "./app/run.sh"]
