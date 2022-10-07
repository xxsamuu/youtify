FROM python:3.9

WORKDIR /youtify/backend

#this section is for being able to update&upgrade system, and doing 'sudo' commands
RUN apt-get update \
 && apt-get install -y sudo
RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker
RUN sudo apt-get update
RUN sudo apt-get install libcups2-dev --yes
RUN sudo apt install build-essential libdbus-glib-1-dev libgirepository1.0-dev --yes

COPY ./code/requirements.txt requirements.txt
RUN pip install wheel && pip install dbus-python
RUN pip install --upgrade setuptools
RUN python3 -m pip install --no-use-pep517  cm-rgb
RUN /usr/local/bin/python -m pip install --upgrade pip&& python3.9 -m pip install -r requirements.txt --no-cache-dir
RUN pip install gevent
COPY ./code .
COPY ./.env .env
RUN ls


EXPOSE 5000
CMD ["python3.9" , "run.py"]
