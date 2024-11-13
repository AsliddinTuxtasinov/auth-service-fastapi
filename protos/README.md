## gRPC Client example
___

```python

import grpc
import user_pb2
import user_pb2_grpc

def run():
    # Connect to the server
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)

    # Test SignUp
    sign_up_request = user_pb2.UserAuthRequest(
        username="+998903908839", password="password123", email="new_user@example.com"
    )
    sign_up_response = stub.SignUp(sign_up_request)
    print(f"SignUp Response: {sign_up_response}")

    # Test Login
    login_request = user_pb2.UserLoginRequest(
        username="+998903908839", password="password123"
    )
    login_response = stub.Login(login_request)
    print(f"Login Response: {login_response}")

    # Test GetUser
    get_user_request = user_pb2.GetUserRequest(token="access new_user")
    get_user_response = stub.GetUser(get_user_request)
    print(f"GetUser Response: {get_user_response}")

if __name__ == '__main__':
    run()
```