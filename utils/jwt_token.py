import os
import datetime
from typing import Dict
from jwcrypto import jwt, jwk
from dotenv import load_dotenv

load_dotenv()


def read_key(file_path: str) -> str:
    with open(file_path, "rb") as key_file:
        return key_file.read().decode("utf-8")


def generate_token_jwt(sub: str) -> Dict[str, str]:
    private_key = read_key(file_path=os.getenv("CERTIFICATE_PRIVATE"))
    public_key = read_key(file_path=os.getenv("CERTIFICATE_PUBLIC"))

    private_jwk = jwk.JWK.from_pem(private_key.encode())
    public_jwk = jwk.JWK.from_pem(public_key.encode())

    now = datetime.datetime.now(datetime.timezone.utc)
    iat = int(now.timestamp())

    payload = {
        "aud": os.getenv("BASE_URL") + os.getenv("AUTH_URL"),
        "sub": sub,
        "iat": iat,
        "exp": int((now + datetime.timedelta(hours=1)).timestamp()),
        "jti": str(iat + 000),
        "ver": "1.1",
    }

    header = {"alg": "RS256"}
    token = jwt.JWT(header=header, claims=payload)
    token.make_signed_token(private_jwk)
    encoded_token = token.serialize()

    decoded_token = jwt.JWT(key=public_jwk, jwt=encoded_token)
    decoded_token.validate(public_jwk)

    return {"token": encoded_token, "iat": iat}
