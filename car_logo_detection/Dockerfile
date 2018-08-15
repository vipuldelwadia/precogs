FROM tensorflow/tensorflow

RUN pip --no-cache-dir install Flask keras requests

EXPOSE 5000

COPY api.py api.py
COPY weights.h5 weights.h5

CMD python api.py