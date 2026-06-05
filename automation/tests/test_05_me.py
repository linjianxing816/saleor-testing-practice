import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION
from graphql.user_queries import ME_QUERY

load_dotenv()


def test_me_query_with_token_should_success(saleor_client):
    email = os.getenv("SALEOR_EMAIL")
    password = os.getenv("SALEOR_PASSWORD")

    login_response = saleor_client.graphql(
        TOKEN_CREATE_MUTATION,
        {
            "email": email,
            "password": password
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert login_data["data"]["tokenCreate"]["errors"] == []

    token = login_data["data"]["tokenCreate"]["token"]

    assert token is not None

    response = saleor_client.graphql(ME_QUERY, token=token)

    assert response.status_code == 200

    data = response.json()

    assert "errors" not in data
    assert data["data"]["me"] is not None
    assert data["data"]["me"]["email"] == email
    assert data["data"]["me"]["isStaff"] is True