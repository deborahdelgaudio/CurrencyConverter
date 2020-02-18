# CurrencyConverter
Web API that offers endpoint `/convert`, to convert currencies using last 90 days conversion rates from [European Central Bank](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml).
The endpoint accepts GET requests with a query string, for more information perform a GET request to `/convert` without any parameter. 
The data source provide conversion rates day by day, so a reference date it's not required for the conversion, the last conversion rate available will be used.

The application can be run into a docker container or locally installing dependencies from `requirments.txt`.

## Docker way :rocket:
Dockerfile included performs installation of dependencies, prepare the database, update the data source, store data into database and run the server.
### Build
The docker image can be built from Dockerfile through:
```
docker build -t container:tag .
```
This will create a container ready to be run called 'container:tag'. You can call it as you want.
### Run
Container can be run by this command:
```
docker run -e PORT=9000 -p 8000:9000 -t container:tag
```
This will perform all the actions written above, so and the end of the process we can use the endpoint on `http://0.0.0.0:8000/convert`
### Tests
Tests are not included on the build process and can be performed by running container on interactive mode.
Run container with interactive mode:
```
docker run -e PORT=9000 -p 8000:9000 -ti container:tag /bin/bash
```
and then run test suite with the following command:
```
python manage.py test
```
##### Requirements:
- Docker


## Local way :house_with_garden:
To run it locally you can installing dependencies using pip from `requirments.txt`. so if you are into the directory you can perfonm
```
pip install -r requirements.txt
``` 
Then `cd converter/` and prepare the database through apply the migrations with:
```
python manage.py migrate
```
Before run the application, update the data source performing a custom django command:
```
python manage.py update_conversion_rates --url https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml
```
Finally you can perform tests:
```
python manage.py test
```
and run server:
```
python manage.py runserver
```
by default the server will be on localhost on port 8000.

##### Requirements:
- python3
- pip


## Data Storage
Data are stored into database performing a custom django command, specified above. By performing it everyday data always be updated.
Database can also be cleaned deleting conversion rates older than X days, this can be performed through:
```python manage.py update_conversion_rates -c 100``` 
This will delete conversion rates older than 100 days. For more information you can digit: `python manage.py update_conversion_rates -h`

#### References
- [Docker](https://docs.docker.com/)
- [python virtualenvs and packages](https://docs.python.org/3/tutorial/venv.html)
- [django](https://docs.djangoproject.com/en/3.0/)
- [django-restframework](https://www.django-rest-framework.org/)
