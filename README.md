# Database Migrations
Alembic is used to handle database migrations. Here are some common commands:
- Generate a new migration (after making changes to the SQLAlchemy models):
    ```shell
    alembic revision --autogenerate -m "{COMMIT MSG}"
    ```
 - Apply migrations:
    ```shell
    alembic upgrade head
    ```
 - Check the current migration status:
    ```shell
     alembic current
     ```
- Downgrade a migration:
    ```shell
    alembic downgrade -1
    ```

# Run server for dev mode
> ```shell
> fastapi dev app
> ```
___
# Run using nginx and docker
```
├───app/
├───db-migration/
├───nginx/
      ├──Dockerfile
      ├──nginx.conf
├───.env
├───requirements.txt
├───Dockerfile
├───docker-compose.yml
```
Example docker-compose.yml
```docker-compose
version: '3.8'

services:
  auth-service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: auth-service
    ports:
      - "6000:8000"  # Host port 6000 mapped to container port 8000
    env_file:
      - .env
    volumes:
      - .:/auth-service
    command: sh -c "uvicorn app.main:app --reload --port=8000 --host=0.0.0.0"

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: auth-service-nginx
    logging:
      options:
        max-size: "10m"
        max-file: "3"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf  # Use the custom Nginx configuration
    ports:
      - "80:80"
    depends_on:
      - auth-service
```
Build and run images by docker-compose
```shell
docker-compose up --build -d
```