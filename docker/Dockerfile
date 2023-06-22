FROM ubuntu:lunar

EXPOSE 8000

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-dev python3-pip python3-venv default-libmysqlclient-dev build-essential netcat-openbsd

WORKDIR /code

COPY .. /code/
RUN mkdir -p exploits

RUN python3 -m venv environment

RUN ./environment/bin/pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["./docker/wait-for.sh", "-t", "0", "database:3306", "--", "./environment/bin/python", "app.py"]