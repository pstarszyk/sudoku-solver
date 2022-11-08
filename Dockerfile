FROM python:3.8.8

WORKDIR /opt/sudoku-solver
ADD . /opt/sudoku-solver

# update APT repos and apply patches
RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y software-properties-common

# install cv2 dependencies
RUN apt-get install -y ffmpeg libsm6 libxext6

# tesseract
RUN add-apt-repository -y ppa:alex-p/tesseract-ocr5 \
    && apt install -y tesseract-ocr

ENV TESSDATA_PREFIX /usr/share/tesseract-ocr/4.00/tessdata

# requirements
RUN pip install --upgrade pip \
    && pip install -r /opt/sudoku-solver/requirements.txt

# permissions
RUN chmod +x /opt/sudoku-solver/app/run.sh

EXPOSE 8001

CMD ["bash", "./app/run.sh"]
