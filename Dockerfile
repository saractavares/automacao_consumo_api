FROM python

WORKDIR /app

COPY ./requirements.txt .

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN apt install -y wget unzip
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/multiarch-support_2.27-3ubuntu1.4_amd64.deb
RUN apt-get install ./multiarch-support_2.27-3ubuntu1.4_amd64.deb
RUN ACCEPT_EULA=Y apt-get -y install msodbcsql17
RUN apt-get -y install unixodbc-dev
RUN apt-get install -y tzdata
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt -f install -y
RUN pip install pyodbc
RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN pip install pip==21.2.3
RUN pip install -r requirements.txt


EXPOSE 80

COPY . .
CMD [ "python","auto.py" ]


