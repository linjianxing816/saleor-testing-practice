import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION

load_dotenv()


def test_token_create_should_return_token(saleor_client):
    email = os.getenv("SALEOR_EMAIL")
    password = os.getenv("SALEOR_PASSWORD")

    response = saleor_client.graphql(
        TOKEN_CREATE_MUTATION,
        {
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "errors" not in data
    assert data["data"]["tokenCreate"]["errors"] == []
    assert data["data"]["tokenCreate"]["token"] is not None
    assert data["data"]["tokenCreate"]["refreshToken"] is not None