FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT 8000

RUN <<EOF
apk update
apk add git
apk add gcc
apk add musl-dev
apk add libffi-dev
EOF

WORKDIR /app 

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . . 

EXPOSE ${PORT}  
ENTRYPOINT ["python3"]
CMD ["-m", "gunicorn", "-c", "gunicorn.conf.py"]
