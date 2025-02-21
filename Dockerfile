FROM python:3.12-slim AS base-container
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt

CMD [ "python3", "app.py"] 
# CMD ["bentoml", "serve", "service:NetworkSecurity"]