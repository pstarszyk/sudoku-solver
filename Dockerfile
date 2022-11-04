FROM python:3.8.8

WORKDIR /opt/sudoku-solver
ADD . /opt/sudoku-solver

# tesseract
RUN apt update \
    && add-apt-repository -y ppa:alex-p/tesseract-ocr5 \
    && apt install -y tesseract-ocr \
    && export "TESSDATA_PREFIX"="/usr/share/tesseract-ocr/4.00/tessdata"

# requirements
RUN pip install --upgrade pip \
    && pip install -r /opt/sudoku-solver/requirements.txt

# permissions
RUN chmod +x /opt/sudoku-solver/run.sh

EXPOSE 8001

CMD ["bash", "./run.sh"]
