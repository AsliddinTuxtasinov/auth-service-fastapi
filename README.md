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

