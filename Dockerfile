FROM python:3.9-slim

EXPOSE 8501

COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install streamlit jaconv

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
