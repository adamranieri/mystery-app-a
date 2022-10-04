FROM python

WORKDIR /code

COPY . /workspace
WORKDIR /workspace
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000" ]