import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION
from graphql.channel_queries import CHANNELS_QUERY
from graphql.product_queries import PRODUCTS_QUERY, PRODUCT_VARIANTS_QUERY
from graphql.checkout_mutations import CHECKOUT_CREATE_MUTATION
from graphql.checkout_queries import CHECKOUT_QUERY

load_dotenv()


def test_checkout_query_after_create_should_success(saleor_client):
    email = os.getenv("SALEOR_EMAIL")
    password = os.getenv("SALEOR_PASSWORD")

    # 第 1 步：登录，获取 token
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
    assert token != ""

    # 第 2 步：查询 channels，提取 channel_slug
    channels_response = saleor_client.graphql(CHANNELS_QUERY, token=token)

    assert channels_response.status_code == 200

    channels_data = channels_response.json()

    assert "errors" not in channels_data
    assert channels_data["data"]["channels"] is not None
    assert len(channels_data["data"]["channels"]) > 0

    channel_slug = channels_data["data"]["channels"][0]["slug"]

    print("提取到的 channel_slug =", channel_slug)

    assert channel_slug is not None
    assert channel_slug != ""

    # 第 3 步：查询 products，提取 product_id
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

    # 第 4 步：查询 variants，提取 variant_id
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

    # 第 5 步：创建 checkout
    checkout_create_response = saleor_client.graphql(
        CHECKOUT_CREATE_MUTATION,
        {
            "channel": channel_slug,
            "variantId": variant_id,
            "quantity": 1
        },
        token=token
    )

    assert checkout_create_response.status_code == 200

    checkout_create_data = checkout_create_response.json()

    print("checkout 创建返回结果 =", checkout_create_data)

    assert "errors" not in checkout_create_data

    checkout_create_result = checkout_create_data["data"]["checkoutCreate"]

    assert checkout_create_result["errors"] == []
    assert checkout_create_result["checkout"] is not None

    created_checkout = checkout_create_result["checkout"]

    checkout_id = created_checkout["id"]
    checkout_token = created_checkout["token"]

    print("创建成功的 checkout_id =", checkout_id)
    print("创建成功的 checkout_token =", checkout_token)

    assert checkout_id is not None
    assert checkout_id != ""

    assert checkout_token is not None
    assert checkout_token != ""

    # 第 6 步：根据 checkout_token 查询 checkout
    checkout_query_response = saleor_client.graphql(
        CHECKOUT_QUERY,
        {
            "token": checkout_token
        },
        token=token
    )

    assert checkout_query_response.status_code == 200

    checkout_query_data = checkout_query_response.json()

    print("checkout 查询返回结果 =", checkout_query_data)

    assert "errors" not in checkout_query_data
    assert checkout_query_data["data"]["checkout"] is not None

    queried_checkout = checkout_query_data["data"]["checkout"]

    assert queried_checkout["id"] == checkout_id
    assert queried_checkout["token"] == checkout_token
    assert queried_checkout["lines"] is not None
    assert len(queried_checkout["lines"]) > 0

    first_line = queried_checkout["lines"][0]

    assert first_line["quantity"] == 1
    assert first_line["variant"]["id"] == variant_id

    print("checkout 查询校验成功，checkout_id =", queried_checkout["id"])