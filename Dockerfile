FROM python:3-alpine

WORKDIR /opt

COPY requirements.txt ./
RUN apk update && apk add curl && \
    pip install --upgrade awscli==1.14.5 && \
    pip install --no-cache-dir -r requirements.txt

COPY main.py ./main.py

EXPOSE 5000

CMD [ "python", "./main.py" ]
