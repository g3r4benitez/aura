# Test Python Aura - Gerardo Benitez
this is a challenge project proposed by daCodes 

see more in [PDF Instructions](./static/test_python_aura.pdf) 

## This project involve

* FastAPI
* Docker
* SQLModel (SqlAchemy)
* RabbitMQ
* Celery
* PostgreSql / SQLite

## Requirements

Python 3.9+

## Project

### Setup environment
1. copy .env.example to .env
2. set environment variables

### Run It: option 1 with docker

1. Start the project 

```sh
docker-compose up
```

### Run It: option 2 manually
1. Start Postgres DB
   ```sh
   docker-compose up postgres
   ```
2. Start api
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requirements.txt
   set -a
   source .env
   set +a
   uvicorn app.main:app --host 0.0.0.0 --port 9009 --reload
   
   ```
3. Start RabbitMq
    ```sh
   docker-compose up rabbit
   ```
4. Start Celery

    in other console
   ```sh
   
   source .venv/bin/activate
   set -a
   source .env
   set +a
   celery -A app.core.celery_worker worker --loglevel=info -Q report_tabs
   
   ```

### Logs
The applications logs are located in 
```
./logs/app.logs
```

### Working

#### Proxy Service
```
curl --request POST 'http://127.0.0.1:9009/categories/MLA97994' 
```

#### Conversations API
```
curl --request GET 'http://127.0.0.1:9009/api/conversations?company=microsoft&tags=competition,orientation' 
```

### Api Documentation
Go to [http://localhost:9009/docs](http://localhost:9009/docs).
![image info](./static/images/docs.png)


## Architecture

![image info](./static/images/arquitecture.png)

## Database

![image info](./static/images/database.png)
