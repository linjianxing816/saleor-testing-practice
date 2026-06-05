import os

from dotenv import load_dotenv

from graphql.auth_mutations import TOKEN_CREATE_MUTATION
from graphql.channel_queries import CHANNELS_QUERY
from graphql.product_queries import PRODUCTS_QUERY, PRODUCT_VARIANTS_QUERY
from graphql.checkout_mutations import (
    CHECKOUT_CREATE_MUTATION,
    CHECKOUT_LINES_UPDATE_MUTATION,
)

load_dotenv()


def test_checkout_update_quantity_should_success(saleor_client):
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

    # 第 5 步：先创建 checkout，初始数量为 1
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

    checkout_token = created_checkout["token"]

    assert checkout_token is not None
    assert checkout_token != ""

    assert created_checkout["lines"] is not None
    assert len(created_checkout["lines"]) > 0
    assert created_checkout["lines"][0]["quantity"] == 1
    assert created_checkout["lines"][0]["variant"]["id"] == variant_id

    print("创建成功的 checkout_token =", checkout_token)

    # 第 6 步：把 checkout 里的商品数量从 1 更新成 2
    update_response = saleor_client.graphql(
        CHECKOUT_LINES_UPDATE_MUTATION,
        {
            "token": checkout_token,
            "variantId": variant_id,
            "quantity": 2
        },
        token=token
    )

    assert update_response.status_code == 200

    update_data = update_response.json()

    print("checkout 数量更新返回结果 =", update_data)

    assert "errors" not in update_data

    update_result = update_data["data"]["checkoutLinesUpdate"]

    assert update_result["errors"] == []
    assert update_result["checkout"] is not None

    updated_checkout = update_result["checkout"]

    assert updated_checkout["token"] == checkout_token
    assert updated_checkout["lines"] is not None
    assert len(updated_checkout["lines"]) > 0

    updated_line = updated_checkout["lines"][0]

    assert updated_line["quantity"] == 2
    assert updated_line["variant"]["id"] == variant_id

    print("checkout 数量更新成功，quantity =", updated_line["quantity"])