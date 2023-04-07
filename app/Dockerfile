FROM python:3.11-alpine3.17
RUN mkdir /app
COPY requirements.txt /app/
RUN python3.11 -m venv /app/.venv
RUN source /app/.venv/bin/activate && pip install -r /app/requirements.txt
COPY main.py /app/
CMD ["/app/.venv/bin/python", "/app/main.py", "hostname -i"]
