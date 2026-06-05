import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION
from graphql.channel_queries import CHANNELS_QUERY

load_dotenv()


def test_extract_channel_slug_should_success(saleor_client):
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

    response = saleor_client.graphql(CHANNELS_QUERY, token=token)

    assert response.status_code == 200

    data = response.json()

    assert "errors" not in data
    assert data["data"]["channels"] is not None
    assert len(data["data"]["channels"]) > 0

    first_channel = data["data"]["channels"][0]

    channel_slug = first_channel["slug"]

    print("提取到的 channel_slug =", channel_slug)

    assert channel_slug is not None
    assert channel_slug != ""