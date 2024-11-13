from __future__ import print_function

import os
import sys

# Add the root directory of the project to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import grpc
from concurrent import futures

import user_pb2
from user_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server

from app.database import get_db
from app.schemas.auth_schemas import UserAuthSchema, UserLoginSchema
from app.utils.authentication.auth_utils import JWTAuthUtils
from app.utils.users import UserUtils

user_utils = UserUtils()
auth_utils = JWTAuthUtils()


class UserService(UserServiceServicer):

    def SignUp(self, request: UserAuthSchema, context):
        try:
            # Call the user creation function with the schema data
            user_utils.create_user_if_not_exists(data=request, db_session=get_db())
            return user_pb2.SignUpResponse(success=True, message="User created successfully")
        except Exception as e:
            context.set_details(f"Failed to create user: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_pb2.SignUpResponse(success=False, message="Error creating user")

    def Login(self, request: UserLoginSchema, context):
        try:
            # Call the user login function with the schema data
            resp_login_schema = user_utils.login_user(data=request, db_session=get_db())
            user_schema = resp_login_schema.user

            return user_pb2.ResponseLogin(
                access=resp_login_schema.access,
                refresh=resp_login_schema.refresh,
                user=user_pb2.User(
                    email=user_schema.email,
                    phone_number=user_schema.phone_number,
                    created_at=user_schema.created_at.isoformat(),
                    is_verified=user_schema.is_verified,
                ),
            )
        except Exception as e:
            context.set_details(f"Failed to login: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_pb2.ResponseLogin()

    def GetUser(self, request, context):
        try:
            # Call to get the user info function with the schema data
            user_id = auth_utils.decode_access_token(token=request.token)
            user_schema = user_utils.get_user(user_id=user_id, db_session=get_db())

            return user_pb2.UserResponse(
                message="User fetched successfully",
                user=user_pb2.User(
                    email=user_schema.email,
                    phone_number=user_schema.phone_number,
                    is_verified=user_schema.is_verified,
                    created_at=user_schema.created_at.isoformat()
                ),
            )

        except Exception as e:
            context.set_details(f"Failed to get user info: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return user_pb2.UserResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')

    print('gRPC server running on port 50051')
    server.start()

    print('gRPC server stopped')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
