FROM python:3.9

COPY server/requirements.txt /server/
RUN python3.9 -m pip install -r /server/requirements.txt --no-cache-dir

COPY server/ /server/
EXPOSE 5000

COPY scripts/run-container.sh .
ENTRYPOINT [ "./run-container.sh" ]
