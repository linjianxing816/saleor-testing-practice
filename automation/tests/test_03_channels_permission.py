from graphql.channel_queries import CHANNELS_QUERY


def test_channels_without_token_should_return_permission_error(saleor_client):
    response = saleor_client.graphql(CHANNELS_QUERY)

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["channels"] is None
    assert "errors" in data
    assert "AUTHENTICATED" in str(data["errors"])