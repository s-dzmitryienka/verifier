Run docker container with DB:
```shell
docker run --name verifier_db -v ~/docker_volumes/verifier_db:/var/lib/postgresql/data -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_DB=verifier-db -e POSTGRES_USER=db_user -e POSTGRES_PASSWORD=db_password -p 5431:5432 -d postgres:12`
```

Start app
```shell
uvicorn main:app --reload
```