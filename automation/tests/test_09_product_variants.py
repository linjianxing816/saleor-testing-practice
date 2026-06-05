import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION
from graphql.channel_queries import CHANNELS_QUERY
from graphql.product_queries import PRODUCTS_QUERY, PRODUCT_VARIANTS_QUERY

load_dotenv()


def test_extract_product_variant_id_should_success(saleor_client):
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

    channel_slug = channels_data["data"]["channels"][0]["slug"]

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

    assert "errors" not in products_data
    assert products_data["data"]["products"] is not None
    assert products_data["data"]["products"]["edges"] is not None
    assert len(products_data["data"]["products"]["edges"]) > 0

    first_product = products_data["data"]["products"]["edges"][0]["node"]

    product_id = first_product["id"]
    product_name = first_product["name"]

    print("提取到的 product_id =", product_id)
    print("提取到的 product_name =", product_name)

    assert product_id is not None
    assert product_id != ""

    variants_response = saleor_client.graphql(
        PRODUCT_VARIANTS_QUERY,
        {
            "id": product_id,
            "channel": channel_slug
        },
        token=token
    )

    assert variants_response.status_code == 200

    variants_data = variants_response.json()

    print("商品 variants 查询返回结果 =", variants_data)

    assert "errors" not in variants_data
    assert variants_data["data"]["product"] is not None
    assert variants_data["data"]["product"]["variants"] is not None
    assert len(variants_data["data"]["product"]["variants"]) > 0

    first_variant = variants_data["data"]["product"]["variants"][0]

    variant_id = first_variant["id"]
    variant_name = first_variant["name"]
    variant_sku = first_variant["sku"]

    print("提取到的 variant_id =", variant_id)
    print("提取到的 variant_name =", variant_name)
    print("提取到的 variant_sku =", variant_sku)

    assert variant_id is not None
    assert variant_id != ""