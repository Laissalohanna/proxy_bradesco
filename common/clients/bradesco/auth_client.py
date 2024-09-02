import os
import requests
from dotenv import load_dotenv


def get_auth_token(jwt_token):
    load_dotenv()
    try:
        payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_token,
        }
        url = os.getenv("BASE_URL") + os.getenv("AUTH_URL")
        print(url)
        response = requests.post(url=url, data=payload, timeout=10)

        if response.status_code != 200:
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            raise requests.exceptions.HTTPError(
                f"Error trying to connect to Bradesco authentication. Status code: {response.status_code}"
            )

        bearer_token = response.json().get("access_token")
        print(bearer_token)
        return bearer_token

    except Exception as e:
        return e
