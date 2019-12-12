FROM python:3.7-slim

COPY ./utils /app/utils/
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./core /app/python/core/
COPY ./flask/server.py /app/server.py

RUN ["python", "utils/data_generator.py", "-o", "products.json"]

ENV INVENTORY products.json

ENTRYPOINT ["python"]
CMD ["server.py"]
