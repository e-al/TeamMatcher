FROM python:3.5-alpine
ADD . /app
WORKDIR /app
RUN pip install -e .
CMD ["flask", "run", "--host=0.0.0.0"]