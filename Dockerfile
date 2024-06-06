FROM ubuntu:24.04
LABEL authors="Raul Agolli webraul.con"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3.12-venv

WORKDIR /app

RUN python3 -m venv venv

COPY requirements.txt .

RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["venv/bin/python", "Main.py", "-s"]


