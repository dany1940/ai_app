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
POSTGRES_PASSWORD=postgres <br />
POSTGRES_DB=postgres <br />
Run the following commands env: <br />
 docker-compose build <br />
 docker-compose up <br />
if everything succesful you can find the sqagger with the endpoints at: <br />
http://0.0.0.0:8000/docs#/ <br />
log in PG4Admin at: <br />
http://localhost:5050/browser/ <br />
create a new server using the above credentials from the env <br />
You should see the migrations and tables, best to use Mozzila or Chrome <br />
If you have MacOs you might be forced to disable the firewall <br />
Download docker interface or use the command line <br />
you should see in docker the api image, pg4admin and postgresql as well as container <br />
Use the swagger to test endpoints <br />
if for some reason you need to restart or rebuild the docker container <br />
please make sure you delete first the migrations, then,  run: <br />
docker-compose down <br />
go in the docker interface and check if any images or conatiners left, if so, just delete all. <br />
then rerun the commands again from docker build onwards <br />









## Contact Information <br />

For any queries about this project, please contact. <br />

- Florin Dumitrascu <gsecomerce@gmail.com> <br />

## Disclaimer <br />

```
Copyright (C) Dany1940 <br />
Unauthorized copying of the files contained in this repository, via any medium is strictly prohibited <br />
Proprietary and confidential <br />
Written by Dumitrascu Florin, June, 2024 <br />
```

