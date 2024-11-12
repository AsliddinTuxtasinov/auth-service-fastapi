from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schemas import UserAuthSchema, UserLoginSchema, ResponseLoginSchema, UserSchema
from app.utils.authentication.auth_utils import JWTAuthUtils
from app.utils.users import UserUtils

user_utils = UserUtils()
auth_utils = JWTAuthUtils()

app = FastAPI(
    title="Auth Service",
    description="Auth Service for JWT Auth Service using JWT Auth Token",
    summary="Auth Service for JWT Auth Service",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Asliddin Tukhtasinov",
        "url": "https://www.linkedin.com/in/asliddintuxtasinov/",
        "email": "asliddintukhtasinov5@gmail.com",
    }
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    path='/signup',
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
    tags=["Auth Service"]
)
async def create_user(data: UserAuthSchema, db: Session = Depends(get_db)):
    return user_utils.create_user_if_not_exists(data=data, db_session=db)


@app.post(
    path='/login',
    summary="Login user",
    status_code=status.HTTP_200_OK,
    response_model=ResponseLoginSchema,
    tags=["Auth Service"]
)
async def login(data: UserLoginSchema, db: Session = Depends(get_db)):
    return user_utils.login_user(data=data, db_session=db)


@app.get(
    path='/get-user',
    summary="get user info",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    tags=["Auth Service"]
)
async def get_user(user_id: str = Depends(auth_utils.decode_access_token), db: Session = Depends(get_db)):
    return user_utils.get_user(user_id=user_id, db_session=db)


@app.get(path="/", status_code=status.HTTP_200_OK, tags=["General"])
async def read_root():
    return {
        "success": True,
        "message": "Hello World!"
    }
