import datetime

import grpc
from concurrent import futures
import user_pb2
from user_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server


class UserService(UserServiceServicer):
    def SignUp(self, request, context):
        # Implement sign-up logic here
        print(f"Sign up method of UserService {request=}")
        return user_pb2.SignUpResponse(success=True, message="User created successfully")

    def Login(self, request, context):
        # Implement login logic here
        print(f"Login method of UserService {request=}")
        return user_pb2.ResponseLogin(
            access="access-token", refresh="refresh-token",
            user=user_pb2.User(
                email="new_user@example.com",
                phone_number=request.phone_number,
                is_verified=False,
                created_at=datetime.datetime.now().isoformat()
            )
        )

    def GetUser(self, request, context):
        # Implement get-user logic here
        print(f"Get User method of UserService {request=}")
        return user_pb2.UserResponse(
            message="User fetched successfully",
            user=user_pb2.User(
                email="new_user@example.com",
                phone_number="1234567890",
                is_verified=False,
                created_at=datetime.datetime.now().isoformat()
            ),
        )


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
