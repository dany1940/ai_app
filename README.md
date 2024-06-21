<h1 align="center">Medical API</h1>
<p align="center">The Api For Medical Connectivity</p>

## Contents

- [Contents](#contents)
- [Contribution](#contribution)
- [Deployment](#deployment)
- [Contact Information](#contact-information)
- [Disclaimer](#disclaimer)


## Contribution

The contents of this GitHub repository is closed source and owned entirely by Dany1940.  Please read CONTRIBUTING.md.

## Deployment

Clone the GitHub Repository <br />
cd in ai_app directory <br />
create a .env file and add <br />
POSTGRES_HOST=db <br />
POSTGRES_USER=postgres <br />
POSTGRES_PORT=5432 <br />
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
Run the following commands env:
 docker-compose build
 docker-compose run web alembic upgrade head
 docker-compose up
if everything succesful you can find the sqagger with the endpoints at:
http://0.0.0.0:8000/docs#/
log in PG4Admin at:
http://localhost:5050/browser/
create a new server using the above credentials from the env
You should see the migrations and tables, best to use Mozzila or Chrome
If you have MacOs you might be forced to disable the firewall
Download docker interface or use the command line
you should see in docker the api image, pg4admin and postgresql as well as container
Use the swagger to test endpoints
if for some reason you need to restart or rebuild the docker container
please make sure you delete first the migrations, then,  run:
docker-compose down
go in the docker interface and check if any images or conatiners left, if so, just delete all.
then rerun the commands again from docker build onwards









## Contact Information

For any queries about this project, please contact.

- Florin Dumitrascu <gsecomerce@gmail.com>

## Disclaimer

```
Copyright (C) Dany1940
Unauthorized copying of the files contained in this repository, via any medium is strictly prohibited
Proprietary and confidential
Written by Dumitrascu Florin, June, 2024
```

