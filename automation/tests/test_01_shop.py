from graphql.shop_queries import SHOP_QUERY


def test_shop_query_success(saleor_client):
    response = saleor_client.graphql(SHOP_QUERY)

    assert response.status_code == 200

    data = response.json()

    assert "errors" not in data
    assert data["data"]["shop"]["name"] is not None