FROM python:3.5
ADD . /app
WORKDIR /app
RUN pip install -e .
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
CMD ["flask", "run", "--host=0.0.0.0"]
