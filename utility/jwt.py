import os
import jwt


def get_token_file(token):
    token_file_path = os.path.join(os.path.dirname(__file__), "../db/token.py")
    with open(token_file_path, "r") as file:
        lines = file.readlines()
    with open(token_file_path, "w") as file:
        for line in lines:
            if line.startswith("jwt_token"):
                file.write(f'jwt_token = "{token}"')
            else:
                file.write(line)


def create_jwt(email):
    """Simulates JWT creation (not implemented)"""
    encoded = jwt.encode({"email": email}, "secret", algorithm="HS256")
    get_token_file(encoded)


def verify_token(token):
    """Simulates JWT token verification and returns the email"""
    decode=jwt.decode(token, "secret", algorithms=["HS256"])
    return decode["email"]


