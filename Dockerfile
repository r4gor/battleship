FROM ubuntu:24.04
LABEL authors="Raul Agolli webraul.con"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "Main.py", "-s"]


