FROM python:alpine
COPY . ./
RUN pip install -r requirements.txt
ENTRYPOINT ["/src/entrypoint.py"]
