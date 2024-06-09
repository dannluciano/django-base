FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT 8000

RUN apk update && \
    apk add git gcc musl-dev libffi-dev

WORKDIR /app 

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . . 

RUN python3 manage.py collectstatic --no-input

EXPOSE ${PORT}  
ENTRYPOINT ["python3"]
CMD ["-m", "gunicorn", "-c", "gunicorn.conf.py"]
