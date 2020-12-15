FROM python:3.8

# Create the working dir
RUN bash -c "mkdir -p /workspace/{eocb,input,output}"

WORKDIR /workspace

# Install dependencies
COPY ./eocb/ ./eocb/
COPY requirements.txt ./eocb/
RUN pip install -r ./eocb/requirements.txt

ENTRYPOINT ["bash", "./eocb/run.sh"]
