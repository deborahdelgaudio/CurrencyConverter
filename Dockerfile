FROM python:3.6
ENV PATH=$PATH:/src/
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY ./converter/ /src/
RUN python manage.py migrate
EXPOSE 8000