import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION
from graphql.channel_queries import CHANNELS_QUERY
from graphql.product_queries import PRODUCTS_QUERY

load_dotenv()


def test_products_query_with_channel_should_success(saleor_client):
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

    channels_response = saleor_client.graphql(CHANNELS_QUERY, token=token)

    assert channels_response.status_code == 200

    channels_data = channels_response.json()

    assert "errors" not in channels_data
    assert channels_data["data"]["channels"] is not None
    assert len(channels_data["data"]["channels"]) > 0

    first_channel = channels_data["data"]["channels"][0]

    channel_slug = first_channel["slug"]

    assert channel_slug is not None
    assert channel_slug != ""

    products_response = saleor_client.graphql(
        PRODUCTS_QUERY,
        {
            "channel": channel_slug
        },
        token=token
    )

    assert products_response.status_code == 200

    products_data = products_response.json()

    print("商品查询返回结果 =", products_data)

    assert "errors" not in products_data
    assert products_data["data"]["products"] is not None
    assert products_data["data"]["products"]["edges"] is not None