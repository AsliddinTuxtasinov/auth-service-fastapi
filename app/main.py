from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schemas import UserAuthSchema
from app.utils.users import UserUtils

app = FastAPI()


@app.post('/signup', summary="Create new user", status_code=status.HTTP_201_CREATED)  # response_model=UserOut
async def create_user(data: UserAuthSchema, db: Session = Depends(get_db)):
    user_utils = UserUtils()
    return user_utils.create_user_if_not_exists(data=data, db_session=db)


@app.get(path="/", status_code=status.HTTP_200_OK)
async def read_root():
    return {
        "success": True,
        "message": "Hello World!"
    }
