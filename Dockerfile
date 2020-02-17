FROM python:3.6
ENV PATH=$PATH:/src/
ENV PORT=$PORT:8000
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY ./converter/ /src/
RUN python manage.py migrate && \
    python manage.py update_conversion_rates --url https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml
EXPOSE $PORT
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:$PORT"]