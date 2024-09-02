import os
from dotenv import load_dotenv
from common.clients.bradesco.auth_client import get_auth_token
from utils.jwt_token import generate_token_jwt


load_dotenv()
token = generate_token_jwt(sub=os.getenv("SECRET_EXTRACT_BALANCE"))
get_bearer_tokens = get_auth_token(jwt_token=token["token"])
