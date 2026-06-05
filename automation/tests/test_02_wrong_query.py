from graphql.error_queries import WRONG_QUERY


def test_wrong_query_should_return_error(saleor_client):
    response = saleor_client.graphql(WRONG_QUERY)

    assert response.status_code == 400

    data = response.json()

    assert "errors" in data
    assert "wrongField" in str(data["errors"])