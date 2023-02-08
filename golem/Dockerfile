FROM python:3.10

RUN pip install torch==1.13.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install diffusers transformers accelerate

COPY txt2img.py /txt2img.py 

RUN python3 txt2img.py --load

RUN which python3

VOLUME /golem/input /golem/output
WORKDIR /golem/work