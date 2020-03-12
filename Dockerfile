FROM python:3.6.10
WORKDIR /etc/apt
RUN mv sources.list ./sources.list.bak
COPY sources.list .
#RUN apt-get update 
#RUN apt-get install libmysql-dev -y
#RUN apt-get install libmysqlclient-dev -y
WORKDIR /app
COPY pl.txt .
COPY . .
RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r pl.txt
CMD python manage.py runserver 0.0.0.0:8000


