FROM 10.103.129.81:5000/opencv3-python
MAINTAINER xiaoxia_yu <xiaoxia_yu@foxitsoftware.com>

RUN mkdir -p /foxitqa
ADD ./imageprocess_pb2.py /foxitqa/imageprocess_pb2.py
ADD ./imageprocess_server.py /foxitqa/imageprocess_server.py
ADD ./fxqaimage.py /foxitqa/fxqaimage.py

WORKDIR /foxitqa

CMD [ "python", "./imageprocess_server.py"] 